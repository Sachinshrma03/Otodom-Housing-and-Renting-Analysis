import pandas as pd
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from snowflake.connector.pandas_tools import pd_writer
import time
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe

start_time = time.time()


engine = create_engine(
    URL(
        account="",  # add your snowflakes account name here
        user="",  # add your username here
        password="",  # add your password here
        database="demo",
        schema="public",
        warehouse="demo_wh",
    )
)

# Connect to the Snowflake database
with engine.connect() as conn:
    try:
        # SQL query to select data from the log table
        query = """ SELECT ID, SPREADSHEET_NAME FROM otodom_data_log """

        # Execute the query and read the result into a Pandas DataFrame
        df = pd.read_sql(query, conn)

        # Convert column names to uppercase
        df.columns = map(lambda x: str(x).upper(), df.columns)

        # Connect to Google Sheets using service account credentials
        gc = gspread.service_account(filename="g-credentials.json")
        loop_counter = 0

        # Iterate through each row in the DataFrame
        for index, row in df.iterrows():
            loop_counter += 1

            # Open the Google Sheets spreadsheet
            locals()["sh" + str(loop_counter)] = gc.open(row["SPREADSHEET_NAME"])
            wks = locals()["sh" + str(loop_counter)].get_worksheet(0)

            # Load the data from the spreadsheet into a DataFrame
            df_out = get_as_dataframe(
                wks,
                usecols=[0, 1, 2],
                nrows=wks.row_count,
                header=None,
                skiprows=1,
                evaluate_formulas=True,
            )
            print(
                "Spreadsheet " + row["SPREADSHEET_NAME"] + " loaded back to DataFrame!"
            )

            # Rename columns and save the DataFrame to a new table in the database
            df_out.columns = ["ID", "TITLE", "TITLE_ENG"]
            df_out.to_sql(
                "otodom_data_flatten_translate",
                con=engine,
                if_exists="append",
                index=False,
                chunksize=16000,
                method=pd_writer,
            )

    except Exception as e:
        # Print an error message if an exception occurs
        print("--- Error --- ", e)
    finally:
        # Close the database connection
        conn.close()

# Dispose of the database engine
engine.dispose()

# Print the total execution time
print("--- %s seconds ---" % (time.time() - start_time))
