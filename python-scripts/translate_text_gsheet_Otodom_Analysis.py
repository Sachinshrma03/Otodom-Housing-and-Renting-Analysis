import pandas as pd
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from snowflake.connector.pandas_tools import pd_writer
import time
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe

start_time = time.time()

# Set up Snowflake database connection
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
        # SQL query to select data from the database
        query = """ SELECT ID, TITLE FROM otodom_data_flatten ORDER BY ID """

        # Execute the query and read the result into a Pandas DataFrame
        df = pd.read_sql(query, conn)

        # Connect to Google Sheets using service account credentials
        gc = gspread.service_account(filename="g-credentials.json")

        loop_counter = 0
        chunk_size = 1000
        file_name = "OTODOM_ANALYSIS_"
        user_email = "sachinshrma.viper@gmail.com"

        # Loop through the DataFrame in chunks
        for i in range(0, len(df), chunk_size):
            loop_counter += 1
            df_in = df.iloc[i : (i + chunk_size), :]

            # Create or open a Google Sheets spreadsheet
            spreadsheet_title = file_name + str(loop_counter)
            try:
                locals()["sh" + str(loop_counter)] = gc.open(spreadsheet_title)
            except gspread.SpreadsheetNotFound:
                locals()["sh" + str(loop_counter)] = gc.create(spreadsheet_title)

            # Share the spreadsheet with a user
            locals()["sh" + str(loop_counter)].share(
                user_email, perm_type="user", role="writer"
            )
            wks = locals()["sh" + str(loop_counter)].get_worksheet(0)
            wks.resize(len(df_in) + 1)
            set_with_dataframe(wks, df_in)

            # Apply a Google Sheets formula to translate text in a specific column
            column = "C"  # Column to apply the formula
            start_row = 2  # Starting row to apply the formula
            end_row = wks.row_count  # Ending row to apply the formula
            cell_range = f"{column}{start_row}:{column}{end_row}"
            curr_row = start_row
            cell_list = wks.range(cell_range)

            for cell in cell_list:
                cell.value = f'=GOOGLETRANSLATE(B{curr_row},"pl","en")'
                curr_row += 1

            # Update the worksheet with the modified cells
            wks.update_cells(cell_list, value_input_option="USER_ENTERED")

            # Print a message indicating the spreadsheet creation
            print(f"Spreadsheet {spreadsheet_title} created!")

            # Log information about the created spreadsheet to a database table
            df_log = pd.DataFrame(
                {"ID": [loop_counter], "SPREADSHEET_NAME": [spreadsheet_title]}
            )
            df_log.to_sql(
                "otodom_data_log",
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
