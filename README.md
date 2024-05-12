# Otodom Housing Analysis Project

This project aims to provide a comprehensive analysis of housing properties listed on the Otodom website, catering to individuals seeking rental or purchase options in Poland. The motivation behind this project arose when a friend was planning to move to Poland, prompting the need for a tool to explore available properties efficiently.

## Project Overview

The Otodom Housing Analysis Project involves scraping property data from the Otodom website, storing it in a database, and performing data transformations and analysis to extract valuable insights. The project utilizes Python scripts for web scraping, data manipulation, and integration with Google Sheets and Snowflake, a cloud-based data warehouse.

## Data Source

The project scrapes data from the Otodom website (https://www.otodom.pl/), which is a popular platform for listing housing properties in Poland. The scraped data includes details such as property ID, title, type (e.g., apartment, house), transaction type (sale or rent), location, price, area, number of rooms, and other relevant information.

## Technologies and Tools Used

- **Programming Languages**: Python, SQL
- **Python Libraries**: requests, csv, logging, pandas, sqlalchemy, gspread, gspread_dataframe
- **Database**: Snowflake (cloud-based data warehouse)
- **Other Tools**: Google Sheets

## Project Structure

The project is organized into the following directories:

- `python_scripts/`: Contains Python scripts for web scraping, data transformation, and integration with Google Sheets and Snowflake.
  - `otodom-scraper.py`: Scrapes property data from the Otodom website.
  - `csv-to-json.py`: Converts the scraped data from CSV to JSON format.
  - `load_data_gsheet_to_SF_Otodom_Analysis.py`: Loads data from Google Sheets into Snowflake.
  - `translate_text_gsheet_Otodom_Analysis.py`: Translates property titles from Polish to English using Google Sheets.
- `sql_queries/`: Contains SQL queries for data transformation and analysis in Snowflake.
  - `sql_queries.txt`: SQL queries for creating stages, tables, and performing data manipulation.
- `data/`: (Optional) Directory to store sample data files or intermediate data files.
- `requirement.txt~`: This file, provides all the required libraries used. 
- `README.md`: This file, provides an overview and instructions for the project.
- `LICENSE`: (Optional) If you plan to release the project under an open-source license.

## Setup and Installation

To run this project, you will need to have the following prerequisites:

1. Python installed on your system.
2. Access to a Snowflake account and the necessary credentials (account name, username, password).
3. A Google account with access to Google Sheets and the ability to generate API credentials.

Follow these steps to set up the project:

1. Clone the repository to your local machine.
2. Install the required Python libraries by running `pip install -r requirements.txt`.
3. Obtain the Snowflake account credentials and update the corresponding fields in the Python scripts.
4. Enable the Google Sheets API for your Google account and generate the necessary API credentials (client secret JSON file).
5. Update the Python scripts with your Google API credentials and the appropriate file paths.

## Usage

To run the project, follow these steps:

1. Execute the `otodom-scraper.py` script to scrape property data from the Otodom website and save it as a CSV file.
2. Run the `csv-to-json.py` script to convert the scraped data from CSV to JSON format.
3. Load the JSON data into Snowflake using the SQL queries provided in `sql_queries.txt`.
4. Execute the `translate_text_gsheet_Otodom_Analysis.py` script to translate property titles from Polish to English using Google Sheets.
5. Run the `load_data_gsheet_to_SF_Otodom_Analysis.py` script to load the translated data from Google Sheets into Snowflake.
6. Perform data analysis and extract insights using SQL queries or BI tools connected to the Snowflake database.

## Data Analysis and Insights

The project provides a foundation for analyzing housing data from the Otodom website. By exploring the transformed and translated data in Snowflake, you can gain insights into various aspects of the housing market, such as:

- Property type distribution (apartments, houses, etc.)
- Price trends and averages for different areas
- Rental vs. sale property statistics
- Popular locations for specific property types
- Correlations between factors like area, number of rooms, and price

You can further extend the analysis by writing additional SQL queries or integrating the data with BI tools to create visualizations and dashboards.

## Future Improvements

Here are some potential improvements that could be considered for this project:

- Implement scheduled scraping to keep the data up-to-date.
- Enhance data cleaning and preprocessing steps for better data quality.
- Integrate additional data sources (e.g., demographic data, neighborhood information) for more comprehensive analysis.
- Develop a user-friendly interface or dashboard for easier data exploration and visualization.
- Implement machine learning models for predictive analytics (e.g., property price prediction).

## Credits and Acknowledgments

This project was inspired by the need to assist a friend in finding suitable housing options in Poland. We would like to acknowledge the following resources and libraries:

- [Otodom](https://www.otodom.pl/) - The website from which property data was scraped.
- [Requests](https://requests.readthedocs.io/en/latest/) - Python library for making HTTP requests.
- [Pandas](https://pandas.pydata.org/) - Python data manipulation and analysis library.
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit and Object-Relational Mapping (ORM) library.
- [gspread](https://gspread.readthedocs.io/en/latest/) - Python library for interacting with Google Sheets.
- [Snowflake](https://www.snowflake.com/) - Cloud-based data warehouse platform.

## License

This project is licensed under the [MIT License](LICENSE).
