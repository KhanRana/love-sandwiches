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
        data_str = input("Enter your data here:\n")
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


# def update_sales_worksheet(data):
#     """
#     Update sales worksheet by adding new line to the sales sheet
#     """
#     print("Updating sales worksheet\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     new_data = [int(value) for value in data]
#     sales_worksheet.append_row(new_data)
#     print("Sales worksheet has been updated successfully.\n")

def update_worksheet(data, work_sheet):
    """
    Update sales worksheet by adding new line to the sales sheet
    """ 
    print(f"Updating {work_sheet} worksheet\n")
    new_sheet = SHEET.worksheet(work_sheet)
    if work_sheet == "sales":
        data = [int(value) for value in data]
    new_sheet.append_row(data)
    print(f"{work_sheet} worksheet has been updated successfully.\n")


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


# def update_surplus_worksheet(surplus_data):
#     """
#     Update surplus worksheep data by calculating it from the latest data
#     """
#     print("Updating suplus worksheet\n")
#     surplus_wroksheet = SHEET.worksheet("surplus")
#     surplus_wroksheet.append_row(surplus_data)
#     print("Surplus sheet has been updated")

def get_last_5_sales():
    """
    this will get last 5 sales data entered by the user
    """
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1, 7):
        column = sales.col_values((ind))
        columns.append(column[-5:])
    return columns


def calsulate_stock_data(data):
    """
    Calculate stock data for the next day 
    and add 10 percent 
    """
    print("Calculating stock data\n")
    new_stock_data = []
    for column in data:
        int_col = [int(number) for number in column]
        average = sum(int_col)/len(int_col)
        stock = average * 1.1
        new_stock_data.append(round(stock))
    return new_stock_data


def main():
    """
    Run all program function
    """
    print("Welcome to automatic stock estimator\n")
    user_data = get_sales_data()
    update_worksheet(user_data, "sales")
    sales_data = user_sales_data()
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sale_data = get_last_5_sales()
    new_stock = calsulate_stock_data(sale_data)
    update_worksheet(new_stock, "stock")


main()
