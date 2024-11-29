# MiaBudget Application v0.2.0

## !!Warning!!
**Please do not share your bank statements when committing a change!**

---

## Project Description:
MiaBudget is an application designed to take multiple bank statements in CSV format and generate a visually appealing PDF budget report that is easy to understand.

---

## Instructions:

### 1. Prepare your Bank's CSV Headers

Before running the application, ensure that the headers in your bank's CSV file are correctly mapped in the banks.json
file. The headers must match the fields used in your bank's statements.

Below is an example structure for banks.json:

{
    "Example_Bank": {
        "Header name for Transaction date": "Date",
        "Header name for transaction name": "Description",
        "Header name for expense": "Expense",
        "Header name for income": "Income",
        "Header name for account balance": "Balance"
    },
    "default": {
        "Date": "Date",
        "Description": "Description",
        "Debit Amount": "Expense",
        "Credit Amount": "Income",
        "Balance": "Balance"
    },
    "AIB": {
        " Posted Transactions Date": "Date",
        " Description1": "Description",
        " Debit Amount": "Expense",
        " Credit Amount": "Income",
        "Balance": "Balance"
    }
}

### 2.  Configure the Settings File

Edit the settings.json file to specify your account name and the bank you’ll be using. In the currency space, only
enter 3 letters. You can also set the time interval for the budget graph.

Example settings.json:

{
    "Config":{
        "AccountName": "Greenlz",
        "Bank": "AIB",         
        "Currency": "EUR",
        "Graph_Interval": "10"
    },

    "Supported Banks":{
        "Allied Irish Bank": "AIB"
    }
}

### 3: Run the Application

Drop your csv files into the input folder and run the main.py script. 

### 4: Create Filters

Open the filter.json and the generated budget.pdf, create your own categories and subcategories in the filter.json

Example filter.json:

{
    "Categoyy":{
        "Subcategory": ["Different", "Listed", "Items"],
        "Subcategory": ["Different", "Listed", "Items"]
    },

    "Income": {
        "Job": "NAL HEALTH"
    },

    "Expenses": {
        "Groceries": ["ASDA", "TESCO", "LIDL"],
        "Restaurants": ["CHARCOAL", "WETHERSPOON", "SUBWAY", "VDC-ISS CARDINAL H"],
        "Coffee": ["STARBUCKS", "FOXY BEAN"],
        "Subscriptions": ["SOLIDWORKS", "D/D"],
        "Partner": ["Revolut", "TransferWise"],
        "Car": ["SPAR", "DAYBREAK","PARKING", "APPLEGREEN"],
        "Online Shopping": ["AMAZON", "STEAMGAMES","AMZN","Twitch", "FACEBK"]
    },

    "Transfers":{
        "Stocks": "Trading"
    },

    "Withdrawals":{
        "ATM": ["VDA", "ATM", "WITHDRAWAL"]
    }
}

### 5: Run the Application Again

Now some uncategorized items are put into a neath category.

Enjoy!

---

## File Functions

### main.py                 =   Script for running everything together
### transaction_processor.py=   Cleanup csv and combine into universal_transactions.csv
### extractor.py            =   Extract the data from the csv using the filter.json
### grapher.py              =   Create the budget.png graph
### pdfer.py                =   Combine all the data into a budget.pdf