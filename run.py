import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

sales = SHEET.worksheet("sales")

data = sales.get_all_values()


def get_sales_data():
    """
    get sales data figures from the user
    """
    print("Please enter the sales data from the last market.")
    print("Data should be six numbers, seperated by commas.")
    print("For example 1,2,3,4,5,6\n")

    data_str = input("Enter your data here: ")
    print(f"You entered: {data_str}")


get_sales_data()
