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
    
    sales_data = data_str.split(',')
    validate_data(sales_data)


def validate_data(values):
    """
    inside the try converts string values into integers,
    raise Valueerror if string cannot be converted into
    integers ro they are not six values.
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you enterd {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")


get_sales_data()
