import json
import csv
import os

def extract_data(csv_file, json_file):
    # Load filter.json
    with open(json_file, 'r') as f:
        filters = json.load(f)
    
    # Initialize data structure for categorized data
    categorized_data = {
        "Income": {},
        "Expenses": {},
        "Transfers": {},
        "Withdrawals": {}
    }
    
    # Process each category in the JSON file
    for main_category, subcategories in filters.items():
        if main_category not in categorized_data:
            categorized_data[main_category] = {}
        for subcategory, keywords in subcategories.items():
            categorized_data[main_category][subcategory] = []

    # Read the CSV file and categorize transactions
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            description = row["Description"].upper()
            expense = float(row["Expense"])
            income = float(row["Income"])
            amount = income if income > 0 else -expense
            
            # Check each category for matching keywords
            for main_category, subcategories in filters.items():
                for subcategory, keywords in subcategories.items():
                    if isinstance(keywords, list):
                        if any(keyword.upper() in description for keyword in keywords):
                            categorized_data[main_category][subcategory].append({
                                "Date": row["Date"],
                                "Description": row["Description"],
                                "Amount": amount
                            })
                    elif isinstance(keywords, str):
                        if keywords.upper() in description:
                            categorized_data[main_category][subcategory].append({
                                "Date": row["Date"],
                                "Description": row["Description"],
                                "Amount": amount
                            })

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
