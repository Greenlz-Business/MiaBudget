import json
import pandas as pd
import glob

class TransactionProcessor:
    def __init__(self, input_folder, output_file, mapping_file, bank="default"):
        """
        Initialize the TransactionProcessor with the input folder, output file path, and mappings.

        Args:
            input_folder (str): The folder containing the CSV files to process.
            output_file (str): The path to save the processed universal CSV file.
            mapping_file (str): The JSON file containing the header mappings.
            bank (str): The key identifying the bank's mapping in the JSON file.
        """
        self.input_folder = input_folder
        self.output_file = output_file
        self.bank = bank

        # Load header mappings from JSON
        with open(mapping_file, 'r') as f:
            mappings = json.load(f)

        # Ensure the bank mapping exists; otherwise, fall back to default
        self.universal_columns = mappings.get(bank, mappings["default"])
        self.headers = list(self.universal_columns.keys())

    def load_csv_files(self):
        """
        Load and concatenate all CSV files matching the pattern in the input folder.

        Returns:
            pd.DataFrame: Concatenated DataFrame from all CSV files.
        """
        csv_path = glob.glob(f"{self.input_folder}/Transaction_Export*.csv")
        if not csv_path:
            raise FileNotFoundError("No files found in the input folder matching the pattern!")
        print(f"Files for bank '{self.bank}' loaded.")
        print("If you get errors below, check if all your csv headers match")
        return pd.concat(
            [pd.read_csv(file, usecols=self.headers, dtype=str) for file in csv_path],
            ignore_index=True
        )

    @staticmethod
    def clean_numeric_columns(df, columns):
        """
        Clean numeric columns by removing commas and converting to numeric values.

        Args:
            df (pd.DataFrame): DataFrame containing the columns to clean.
            columns (list of str): List of column names to clean.

        Returns:
            pd.DataFrame: Updated DataFrame with cleaned numeric columns.
        """
        for column in columns:
            df[column] = pd.to_numeric(df[column].str.replace(',', '', regex=True), errors='coerce').fillna(0)
        return df

    def process_transactions(self):
        """
        Process the transactions by loading, cleaning, sorting, and saving the data.

        Returns:
            None
        """
        # Load and combine data from CSV files
        df = self.load_csv_files()

        # Clean numeric columns
        numeric_columns = [' Credit Amount', ' Debit Amount', 'Balance']
        df = self.clean_numeric_columns(df, numeric_columns)

        # Rename and select universal columns
        universal_df = df.rename(columns=self.universal_columns)

        # Sort by date in ascending order
        universal_df['Date'] = pd.to_datetime(universal_df['Date'], format='%d/%m/%Y', errors='coerce')
        universal_df = universal_df.sort_values(by='Date').reset_index(drop=True)

        # Remove rows with duplicate Date, Expense, Income, and Balance
        universal_df = universal_df.drop_duplicates(subset=['Date', 'Expense', 'Income', 'Balance'], keep='first')

        # Save to a new CSV file
        universal_df.to_csv(self.output_file, index=False)
        print(f"Universal transactions saved successfully to {self.output_file}.")

if __name__ == "__main__":
    
    with open("settings.json", "r") as f:
        settings_data = json.load(f)
    mybank = settings_data.get("Config", {}).get("Bank", "DefaultBank")     # Useful 
    
    processor = TransactionProcessor(
        input_folder = "input",
        output_file = "universal_transactions.csv",
        mapping_file = "banks.json",
        bank = mybank  # Change to the desired bank key
    )
    try:
        processor.process_transactions()
    except FileNotFoundError as e:
        print(e)
