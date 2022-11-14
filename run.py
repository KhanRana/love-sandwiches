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


def get_sales_data():
    """
    get sales data figures from the user
    """
    while True:
        print("Please enter the sales data from the last market.")
        print("Data should be six numbers, seperated by commas.")
        print("For example 1,2,3,4,5,6\n")
        
        data_str = input("Enter your data here: ")
        
        sales_data = data_str.split(',')
        
        if validate_data(sales_data):
            print("Valid data!")
            break

    return sales_data


def validate_data(values):
    """
    inside the try converts string values into integers,
    raise Valueerror if string cannot be converted into
    integers ro they are not six values.
    """
    try:
        data_check = [int(value) for value in values]
        if len(data_check) != 6:
            raise ValueError(
                f"Exactly 6 values required, you enterd {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False   
    return True


def update_sales_worksheet(data):
    """
    Update sales worksheet by adding new line to the sales sheet
    """
    print("Updating sales worksheet\n")
    sales_worksheet = SHEET.worksheet("sales")
    new_data = [int(value) for value in data]
    sales_worksheet.append_row(new_data)
    print("Sales worksheet has been updated successfully.\n")


user_data = get_sales_data()
update_sales_worksheet(user_data)


