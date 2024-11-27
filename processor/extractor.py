from datetime import datetime
import json
import csv
import os
from collections import defaultdict

def extract_data(csv_file, json_file):
    # Load filter.json
    with open(json_file, 'r') as f:
        filters = json.load(f)
    
    # Initialize data structure for categorized data
    categorized_data = {
        "Statistics": {
            "Total Income": 0.0,
            "Total Expenses": 0.0,
            "Total Transactions": 0,
            "Starting Balance": 0.0,
            "Ending Balance": 0.0,
            "Average Daily Spending": 0.0,
            "Average Daily Income": 0.0,
            "Most Expensive Day": {"Date": None, "Amount": 0.0},
            "Item with Highest Total Spending": {"Description": None, "Total Amount": 0.0}
        },
        "Income": {},
        "Expenses": {},
        "Transfers": {},
        "Withdrawals": {}
    }
    
    # Dictionary to track daily expenses
    daily_expenses = {}
    
    # Dictionary to track total spending on each item
    item_totals = defaultdict(float)

    # Process each category in the JSON file
    for main_category, subcategories in filters.items():
        if main_category not in categorized_data:
            categorized_data[main_category] = {}
        for subcategory, keywords in subcategories.items():
            categorized_data[main_category][subcategory] = []

    # Read the CSV file and categorize transactions
    transactions = []
    unique_dates = set()
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row["Date"]
            description = row["Description"]
            expense = float(row["Expense"])
            income = float(row["Income"])
            balance = float(row["Balance"])
            amount = income if income > 0 else -expense

            # Track transactions and dates for balance and spending calculation
            transactions.append(balance)
            unique_dates.add(date)

            # Track daily expenses
            if expense > 0:
                if date not in daily_expenses:
                    daily_expenses[date] = 0.0
                daily_expenses[date] += expense
                
                # Track total spending for each item
                item_totals[description] += expense

            # Update statistics
            if income > 0:
                categorized_data["Statistics"]["Total Income"] += income
            if expense > 0:
                categorized_data["Statistics"]["Total Expenses"] += expense

            # Increment total transactions count
            categorized_data["Statistics"]["Total Transactions"] += 1

            # Check each category for matching keywords
            for main_category, subcategories in filters.items():
                for subcategory, keywords in subcategories.items():
                    if isinstance(keywords, list):
                        if any(keyword.upper() in description.upper() for keyword in keywords):
                            categorized_data[main_category][subcategory].append({
                                "Date": date,
                                "Description": description,
                                "Amount": amount
                            })
                    elif isinstance(keywords, str):
                        if keywords.upper() in description.upper():
                            categorized_data[main_category][subcategory].append({
                                "Date": date,
                                "Description": description,
                                "Amount": amount
                            })

    # Calculate starting and ending balances
    if transactions:
        categorized_data["Statistics"]["Starting Balance"] = round(transactions[0], 2)
        categorized_data["Statistics"]["Ending Balance"] = round(transactions[-1], 2)

    # Calculate average daily spending and income
    if unique_dates:
        num_days = len(unique_dates)
        categorized_data["Statistics"]["Average Daily Spending"] = round(
            categorized_data["Statistics"]["Total Expenses"] / num_days, 2
        )
        categorized_data["Statistics"]["Average Daily Income"] = round(
            categorized_data["Statistics"]["Total Income"] / num_days, 2
        )

    # Find the most expensive day
    if daily_expenses:
        most_expensive_day = max(daily_expenses.items(), key=lambda x: x[1])
        categorized_data["Statistics"]["Most Expensive Day"] = {
            "Date": most_expensive_day[0],
            "Amount": round(most_expensive_day[1], 2)
        }

    # Find the item with the highest total spending
    if item_totals:
        highest_spending_item = max(item_totals.items(), key=lambda x: x[1])
        categorized_data["Statistics"]["Item with Highest Total Spending"] = {
            "Description": highest_spending_item[0],
            "Total Amount": round(highest_spending_item[1], 2)
        }

    return categorized_data

# Example usage
if __name__ == "__main__":
    csv_file = "universal_transactions.csv"
    json_file = "filter.json"
    data = extract_data(csv_file, json_file)
    
    # Save categorized data as JSON in the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "categorized_data.json")
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
    
    # Print the location of the saved file
    print(f"Categorized data saved to: {output_file}")
