import json
from fpdf import FPDF
import pandas as pd
from datetime import datetime
import csv

# Get the current time and date
now = datetime.now()
formatted_time_date = now.strftime("%H:%M:%S,       %d, %b, %Y")  # Time and Date

# Load and process date range from the CSV
def load_date_range(csv_file):
    df = pd.read_csv(csv_file)
    df['Date'] = pd.to_datetime(df['Date'])
    newest_date = df['Date'].max()
    oldest_date = df['Date'].min()
    return oldest_date.strftime("%d-%b-%Y"), newest_date.strftime("%d-%b-%Y")

# Load settings
def load_settings():
    with open("settings.json", "r") as file:
        settings = json.load(file)
    account_name = settings["Config"]["AccountName"]
    bank_format = settings["Config"]["Bank"]
    currency = settings["Config"]["Currency"]
    return account_name, bank_format, currency

# Load Categorized Data Json
def load_categorized_data():
    with open("categorized_data.json", "r") as file:
        data = json.load(file)
    total_income = f"{data['Statistics']['Total Income']:,.2f}"
    total_expense = f"{data['Statistics']['Total Expenses']:,.2f}"
    total_transactions = data["Statistics"]["Total Transactions"]
    total_outcome = f"{(data['Statistics']['Total Income']) - (data['Statistics']['Total Expenses']):,.2f}"     # Outcome = Cashflow
    starting_balance = data["Statistics"]["Starting Balance"]
    ending_balance = data["Statistics"]["Ending Balance"]
    daily_spending = data["Statistics"]["Average Daily Spending"]
    daily_income = data["Statistics"]["Average Daily Income"]
    
    most_expensive_day = data['Statistics'].get('Most Expensive Day', {})
    expensive_date = most_expensive_day.get('Date', 'N/A')
    expensive_amount = f"{most_expensive_day.get('Amount', 0):,.2f}"
    
    # Format the date if it's not 'N/A'
    if expensive_date != 'N/A':
        try:
            parsed_date = datetime.strptime(expensive_date, "%Y-%m-%d")
            expensive_date = parsed_date.strftime("%d, %b, %Y")  
        except ValueError:
            expensive_date = "Invalid Date"
    
    total_item = data['Statistics'].get('Item with Highest Total Spending', {})
    total_item_desc = total_item.get('Description', 'N/A')
    total_item_amount = f"{total_item.get('Total Amount', 'N/A'):,.2f}"
    
    return total_income, total_expense, total_transactions, total_outcome, starting_balance, ending_balance, daily_spending, daily_income, expensive_date, expensive_amount, total_item_desc, total_item_amount
    
# Cover
def add_cover_page(pdf, w):
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 30)
    pdf.set_xy(((w/2)-(70/2)), 100)
    pdf.cell(70, 20, 'MiaBudget', border=1, align='C')
    pdf.set_xy(((w/2)-(70/2)), 125)
    pdf.set_font('helvetica', 'I', 15)
    pdf.cell(70, 12, 'Created by GreenLz', border=0, align='C')

# 1 Page
def add_disclaimer_page(pdf, w):
    pdf.add_page()
    pdf.set_xy(((w/2)-(70/2)), 13)
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(70, 15, 'Disclaimer', border=0, align='C')
    pdf.set_xy(25, 60)
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(w-50, 7, R"This budget app is a personal project designed to convert bank statements into easy-to-understand budget reports with graphs. While every effort has been made to ensure the accuracy of the generated PDF file, errors may occur in the processing of data. The viewer is advised to double-check the budget details and confirm the accuracy of the information presented. The app creator is not responsible for any financial errors or discrepancies resulting from the use of this tool.", border=0, align='J')

# 2 Page
def add_overview_page(pdf, w, oldest_date_str, newest_date_str, account_name, bank_format, currency, total_transactions, total_income, total_expense, total_outcome, starting_balance, ending_balance, daily_spending, daily_income, expensive_date, expensive_amount, total_item_desc, total_item_amount):
    pdf.add_page()
    pdf.set_xy(((w/2)-(70/2)), 13)                          # Header
    pdf.set_font('helvetica', 'B', 16)                      # Header
    pdf.cell(70, 15, 'Overview', border=0, align='C')       # Header
    pdf.set_xy(((w/2)-(100/2)), 35)                                                                 # Budget Date
    pdf.set_font('helvetica', 'I', 13)                                                              # Budget Date
    pdf.cell(95, 13, f'Budget from {oldest_date_str} to {newest_date_str}', align='C', border=1)    # Budget Date
    
    pdf.set_font('helvetica', 'B', 13)                          # Account Name
    pdf.set_xy(20, 70)                                          # Account Name
    pdf.cell(40, 10, 'Account Name:', border=0, align='L')      # Account Name     
    pdf.set_font('helvetica', '', 13)                           # Account Name
    pdf.set_xy(70, 70)                                          # Account Name
    pdf.cell(120, 10, account_name, border=0, align='C')        # Account Name
    pdf.set_font('helvetica', 'B', 13)                          # Bank Format
    pdf.set_xy(20, 80)                                          # Bank Format
    pdf.cell(40, 10, 'Bank Format:', border=0, align='L')       # Bank Format  
    pdf.set_font('helvetica', '', 13)                           # Account Name
    pdf.set_xy(70, 80)                                          # Account Name
    pdf.cell(120, 10, bank_format, border=0, align='C')         # Account Name
    pdf.set_font('helvetica', 'B', 13)                          # Currency
    pdf.set_xy(20, 90)                                          # Currency
    pdf.cell(40, 10, 'Currency:', border=0, align='L')          # Currency 
    pdf.set_font('helvetica', '', 13)                           # Currency
    pdf.set_xy(70, 90)                                          # Currency
    pdf.cell(120, 10, currency, border=0, align='C')            # Currency
    pdf.set_font('helvetica', 'B', 13)                                      # Transactions Amount
    pdf.set_xy(20, 110)                                                     # Transactions Amount
    pdf.cell(40, 10, 'Amount of Transactions:', border=0, align='L')           # Transactions Amount 
    pdf.set_font('helvetica', '', 13)                                       # Transactions Amount
    pdf.set_xy(70, 110)                                                     # Transactions Amount
    pdf.cell(120, 10, str(total_transactions), border=0, align='C')         # Transactions Amount
    pdf.set_font('helvetica', 'B', 13)                                      # Total Income
    pdf.set_xy(20, 120)                                                     # Total Income
    pdf.cell(40, 10, 'Total Income:', border=0, align='L')                  # Total Income 
    pdf.set_font('helvetica', '', 13)                                                        # Total Income
    pdf.set_xy(70, 120)                                                                      # Total Income
    pdf.cell(120, 10, str(total_income) + " " + currency, border=0, align='C')               # Total Income
    pdf.set_font('helvetica', 'B', 13)                                      # Total Expense
    pdf.set_xy(20, 130)                                                     # Total Expense
    pdf.cell(40, 10, 'Total Expense:', border=0, align='L')                 # Total Expense
    pdf.set_font('helvetica', '', 13)                                                        # Total Expense
    pdf.set_xy(70, 130)                                                                      # Total Expense
    pdf.cell(120, 10, str(total_expense) + " " + currency, border=0, align='C')              # Total Expense
    pdf.set_font('helvetica', 'B', 13)                                      # Total Outcome
    pdf.set_xy(20, 140)                                                     # Total Outcome
    pdf.cell(40, 10, 'Total Cashflow:', border=0, align='L')                 # Total Outcome
    pdf.set_font('helvetica', '', 13)                                                        # Total Outcome
    pdf.set_xy(70, 140)                                                                      # Total Outcome
    pdf.cell(120, 10, str(total_outcome) + " " + currency, border=0, align='C')              # Total Outcome
    pdf.set_font('helvetica', 'B', 13)                                          # Opening Balance
    pdf.set_xy(20, 160)                                                         # Opening Balance
    pdf.cell(40, 10, 'Opening Balance:', border=0, align='L')                   # Opening Balance
    pdf.set_font('helvetica', '', 13)                                                        # Opening Balance
    pdf.set_xy(70, 160)                                                                      # Opening Balance
    pdf.cell(120, 10, str(starting_balance) + " " + currency, border=0, align='C')           # Opening Balance
    pdf.set_font('helvetica', 'B', 13)                                          # Ending Balance
    pdf.set_xy(20, 170)                                                         # Ending Balance
    pdf.cell(40, 10, 'Closing Balance:', border=0, align='L')                   # Ending Balance
    pdf.set_font('helvetica', '', 13)                                                        # Ending Balance
    pdf.set_xy(70, 170)                                                                      # Ending Balance
    pdf.cell(120, 10, str(ending_balance) + " " + currency, border=0, align='C')              # Ending Balance
    pdf.set_font('helvetica', 'B', 13)                                                  # Average Daily income
    pdf.set_xy(20, 190)                                                                 # Average Daily income
    pdf.cell(40, 10, 'Average Daily Income:', border=0, align='L')                    # Average Daily income
    pdf.set_font('helvetica', '', 13)                                                        # Average Daily income
    pdf.set_xy(70, 190)                                                                      # Average Daily income
    pdf.cell(120, 10, str(daily_income) + " " + currency, border=0, align='C')              # Average Daily income
    pdf.set_font('helvetica', 'B', 13)                                                  # Average Daily Spending
    pdf.set_xy(20, 200)                                                                 # Average Daily Spending
    pdf.cell(40, 10, 'Average Daily Spending:', border=0, align='L')                    # Average Daily Spending
    pdf.set_font('helvetica', '', 13)                                                        # Average Daily Spending
    pdf.set_xy(70, 200)                                                                      # Average Daily Spending
    pdf.cell(120, 10, str(daily_spending) + " " + currency, border=0, align='C')              # Average Daily Spending
    pdf.set_font('helvetica', 'B', 13)                                                  # Average Daily Spending
    pdf.set_xy(20, 210)                                                                 # Average Daily Spending
    pdf.cell(40, 10, 'Average Daily Cashflow:', border=0, align='L')                    # Average Daily Spending
    pdf.set_font('helvetica', '', 13)                                                        # Average Daily Spending
    pdf.set_xy(70, 210)                                                                      # Average Daily Spending
    pdf.cell(120, 10, str(daily_income-daily_spending) + " " + currency, border=0, align='C')              # Average Daily Spending
    pdf.set_font('helvetica', 'B', 13)                                                  # Most Expensive Day and Amount
    pdf.set_xy(20, 230)                                                                 # Most Expensive Day and Amount
    pdf.cell(40, 10, 'Most Expensive Day & Amount:', border=0, align='L')                    # Most Expensive Day and Amount
    pdf.set_font('helvetica', '', 13)                                                                       # Most Expensive Day and Amount
    pdf.set_xy(70, 230)                                                                                     # Most Expensive Day and Amount
    pdf.cell(120, 10,  expensive_date + "   " + str(expensive_amount) + " " + currency, border=0, align='C')               # Most Expensive Day and Amount
    
    pdf.set_font('helvetica', 'B', 13)                                                  # Most Expensive Item
    pdf.set_xy(20, 240)                                                                 # Most Expensive Item
    pdf.cell(40, 10, 'Item with Highest Total:', border=0, align='L')                    # Most Expensive Item
    
    pdf.set_font('helvetica', '', 13)                                                                       # Most Expensive Item
    pdf.set_xy(70, 240)                                                                                     # Most Expensive Item
    pdf.cell(120, 10,  total_item_desc, border=0, align='C')               # Most Expensive Item
    
    pdf.set_font('helvetica', 'B', 13)                                                  # Most Expensive Item
    pdf.set_xy(20, 250)                                                                 # Most Expensive Item
    pdf.cell(40, 10, 'Total Spent on Item:', border=0, align='L')                    # Most Expensive Item
    
    pdf.set_font('helvetica', '', 13)                                                                       # Most Expensive Item
    pdf.set_xy(70, 250)                                                                                     # Most Expensive Item
    pdf.cell(120, 10,  str(total_item_amount) + " " + currency, border=0, align='C')               # Most Expensive Item
    
    
    pdf.set_font('helvetica', 'B', 13)                                                  # Time and Date
    pdf.set_xy(20, 55)                                                                 # Time and Date
    pdf.cell(40, 10, 'Time and Date of Report:', border=0, align='L')                   # Time and Date
    pdf.set_font('helvetica', 'I', 13)                                                  # Time and Date
    pdf.set_xy(70, 55)                                                                # Time and Date
    pdf.cell(120, 10, formatted_time_date, border=0, align='C')                        # Time and Date
    
# 3 Page
def add_budgetgraph_page(pdf, w):
    pdf.add_page()
    pdf.set_xy(((w/2)-35), 13)
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(75, 15, 'Budget Graph', border=0, align='C')
    pdf.image("budgetgraph.jpg", w=178, x=15, y=90)
    
# Other Pages
def add_other_pages(pdf, w):
    with open("categorized_data.json", "r") as file:
        data = json.load(file)

    categories = ["Income", "Expenses", "Transfers", "Withdrawals"]
    uncategorized = data.get("Uncategorized", [])  # Get uncategorized transactions
    pdf.add_page()
    pdf.set_xy(((w / 2) - (70 / 2)), 13)
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(70, 15, 'Budget Breakdown', border=0, align='C')

    y_position = 30  # Start position for the table content
    page_number = 4  # Starting page number for this section

    # Helper function to format dates
    def format_date(date_str):
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%d, %b, %Y")
        except ValueError:
            return "Invalid Date"

    # Iterate over categories
    for category in categories:
        if category in data:
            # Category Header
            if y_position > 260:
                pdf.add_page()
                y_position = 20
                page_number += 1

            pdf.set_xy(20, y_position)
            pdf.set_font('helvetica', 'B', 14)
            pdf.cell(170, 10, category, border=1, align='C')
            y_position += 10

            # Subcategories and their transactions
            for subcategory, transactions in data[category].items():
                if transactions:  # Ensure the subcategory has transactions
                    if y_position > 260:
                        pdf.add_page()
                        y_position = 20
                        page_number += 1

                    pdf.set_xy(20, y_position)
                    pdf.set_font('helvetica', 'B', 11)
                    pdf.cell(170, 10, subcategory, border=0, align='L')
                    y_position += 10

                    # Transactions within the subcategory
                    for transaction in transactions:
                        if y_position > 260:
                            pdf.add_page()
                            y_position = 20
                            page_number += 1

                        pdf.set_xy(20, y_position)
                        pdf.set_font('helvetica', '', 10)
                        formatted_date = format_date(transaction["Date"])
                        pdf.cell(30, 10, formatted_date, border=0, align='C')
                        pdf.cell(100, 10, transaction["Description"], border=0, align='L')
                        pdf.cell(40, 10, f"{transaction['Amount']:,.2f}", border=0, align='R')
                        y_position += 10

    # Add uncategorized transactions section
    if uncategorized:
        if y_position > 260:
            pdf.add_page()
            y_position = 20
            page_number += 1

        # Uncategorize Header
        pdf.set_xy(20, y_position)
        pdf.set_font('helvetica', 'B', 14)
        pdf.cell(170, 10, 'Uncategorized Transactions', border=1, align='C')
        y_position += 10

        # Adding uncategorized transactions to the table
        for transaction in uncategorized:
            if y_position > 260:
                pdf.add_page()
                y_position = 20
                page_number += 1

            pdf.set_xy(20, y_position)
            pdf.set_font('helvetica', '', 10)
            formatted_date = format_date(transaction["Date"])
            pdf.cell(30, 10, formatted_date, border=0, align='C')
            pdf.cell(100, 10, transaction["Description"], border=0, align='L')
            pdf.cell(40, 10, f"{transaction['Amount']:,.2f}", border=0, align='R')
            y_position += 10

# Main script
def create_pdf(output_file, csv_file):
    oldest_date_str, newest_date_str = load_date_range(csv_file)
    pdf = FPDF('P', 'mm', 'A4')
    w, h = 210, 297
    account_name, bank_format, currency = load_settings()
    total_income, total_expense, total_transactions, total_outcome, starting_balance, ending_balance, daily_spending, daily_income, expensive_date, expensive_amount, total_item_desc, total_item_amount = load_categorized_data()

    add_cover_page(pdf, w)
    add_disclaimer_page(pdf, w)
    add_overview_page(pdf, w, oldest_date_str, newest_date_str, account_name, bank_format, currency, total_transactions, total_income, total_expense, total_outcome, starting_balance, ending_balance, daily_spending, daily_income, expensive_date, expensive_amount, total_item_desc, total_item_amount)
    add_budgetgraph_page(pdf, w)
    add_other_pages(pdf, w)

    pdf.output(output_file)

# Generate the PDF
create_pdf('Budget.pdf', 'universal_transactions.csv')
