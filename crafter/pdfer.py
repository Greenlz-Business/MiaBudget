import json
from fpdf import FPDF
import pandas as pd
from datetime import datetime
import csv

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
    pdf.set_xy(10, 275)
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 1, '1', border=0, align='C')

# 2 Page
def add_overview_page(pdf, w, oldest_date_str, newest_date_str, account_name, bank_format, currency):
    pdf.add_page()
    pdf.set_xy(((w/2)-(70/2)), 13)                          # Header
    pdf.set_font('helvetica', 'B', 16)                      # Header
    pdf.cell(70, 15, 'Overview', border=0, align='C')       # Header
    pdf.set_xy(((w/2)-(100/2)), 35)                                                                 # Budget Date
    pdf.set_font('helvetica', 'I', 13)                                                              # Budget Date
    pdf.cell(95, 13, f'Budget from {oldest_date_str} to {newest_date_str}', align='C', border=1)    # Budget Date
    
    pdf.set_font('helvetica', 'B', 13)                          # Account Name
    pdf.set_xy(20, 70)                                          # Account Name
    pdf.cell(40, 10, 'Account Name:', border=1, align='C')      # Account Name     
    pdf.set_font('helvetica', '', 13)                           # Account Name
    pdf.set_xy(70, 70)                                          # Account Name
    pdf.cell(120, 10, account_name, border=1, align='L')        # Account Name
    
    pdf.set_font('helvetica', 'B', 13)                          # Bank Format
    pdf.set_xy(20, 80)                                          # Bank Format
    pdf.cell(40, 10, 'Bank Format:', border=1, align='C')       # Bank Format  
    
    pdf.set_font('helvetica', '', 13)                           # Account Name
    pdf.set_xy(70, 80)                                          # Account Name
    pdf.cell(120, 10, bank_format, border=1, align='L')         # Account Name
    
    pdf.set_font('helvetica', 'B', 13)                          # Currency
    pdf.set_xy(20, 90)                                          # Currency
    pdf.cell(40, 10, 'Currency:', border=1, align='C')           # Currency 
    
    pdf.set_font('helvetica', '', 13)                           # Account Name
    pdf.set_xy(70, 90)                                          # Account Name
    pdf.cell(120, 10, currency, border=1, align='L')            # Account Name
    
    
    
    pdf.set_xy(10, 275)                                 # Page number
    pdf.set_font('helvetica', '', 12)                   # Page number
    pdf.cell(0, 1, '2', border=0, align='C')            # Page number

# 3 Page
def add_budgetgraph_page(pdf, w):
    pdf.add_page()
    pdf.set_xy(((w/2)-(70/2)), 13)
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(70, 15, 'Budget Graph', border=0, align='C')
    pdf.image("budgetgraph.jpg", w=172, x=20, y=70)
    pdf.set_xy(10, 275)
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 1, '3', border=0, align='C')

# Main script
def create_pdf(output_file, csv_file):
    oldest_date_str, newest_date_str = load_date_range(csv_file)
    pdf = FPDF('P', 'mm', 'A4')
    w, h = 210, 297
    account_name, bank_format, currency = load_settings()

    add_cover_page(pdf, w)
    add_disclaimer_page(pdf, w)
    add_overview_page(pdf, w, oldest_date_str, newest_date_str, account_name, bank_format, currency)
    add_budgetgraph_page(pdf, w)

    pdf.output(output_file)

# Generate the PDF
create_pdf('Budget.pdf', 'universal_transactions.csv')
