import gspread
from google.oauth2.service_account import Credentials
# from pprint import pprint

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


def user_sales_data():
    """
    get sales data from the sheet that user entered
    """
    new_sales = SHEET.worksheet("sales").get_values()
    sales_row = new_sales[-1]
    return sales_row


def calculate_surplus_data(sales_row):
    """
    Compare stock with sales and calculate surplus
    surplus = stock - sales
    """
    print("Calculating surplus data\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = (stock[-1])
    stock_data = [int(stock) for stock in stock_row]

    surplus_data = []
    for stock, sales in zip(stock_data, sales_row):
        surplus = stock - int(sales)
        surplus_data.append(surplus)
    
    return surplus_data


def update_surplus_worksheet(surplus_data):
    """
    Update surplus worksheep data by calculating it from the latest data
    """
    print("Updating suplus worksheet\n")
    surplus_wroksheet = SHEET.worksheet("surplus")
    surplus_wroksheet.append_row(surplus_data)
    print("Surplus sheet has been updated")


def main():
    """
    Run all program function
    """
    user_data = get_sales_data()
    update_sales_worksheet(user_data)
    sales_data = user_sales_data()
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)
    update_surplus_worksheet(new_surplus_data)


main()
