from dbmanagement.access_data import DBManager
import os
import datetime
from src import ProjectConstants


def load_sql_data(inputted_providers_list: list, number_of_test_days: int = 30) -> None:
    """Function that reads the SQL file and get the updated data within the shifted last 365 + test days.
    Args:
    number_of_test_days: Number of days will be tested once the model built. Default value is 30 days.

    Return: None
    """

    # Find the starting date
    starting_date = (
        datetime.datetime.now() - datetime.timedelta(days=365 + number_of_test_days)
    )
    starting_date_string = starting_date.strftime("%Y/%m/%d")
    print(
        f"SQL data retrival process initiated with the starting date: {starting_date_string} and number of test days: {number_of_test_days}.")

    # Read SQL Query file within the same directory
    get_data_file_path = os.path.dirname(__file__)
    with open(get_data_file_path + "/provider_satis.sql", "r") as rd:
        sql_query_text = rd.read().replace("\n", " ").replace("%H", "%%H")

    # Add "%s" characters as many as the number of providers, in the corresponding part of the query
    placeholder_provider_list = ["%s" for _ in inputted_providers_list]
    providers_list_query_str = "(" + ", ".join(placeholder_provider_list) + ")"
    sql_query_text = sql_query_text.replace(":providers_list", providers_list_query_str)

    # Connect to weg_flight DB and get the updated data
    conn = DBManager(mysql_db="weg_flight")
    data = conn.get_mysql_data(
        sql=sql_query_text, params=(starting_date_string, *inputted_providers_list))
    data.to_csv(ProjectConstants.ROOT_DIR + "/data/" +
                "provider_data.csv", index=False)

    print(data.head())
    extracted_providers_list = data.provider.unique().tolist()
    print("Inputted list of providers include: ", sorted(inputted_providers_list), " with total number of: ", len(inputted_providers_list))
    print("Extracted list of providers include: ", sorted(extracted_providers_list), " with total number of: ", len(extracted_providers_list))