import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the Universal DataFrame
df = pd.read_csv('universal_transactions.csv')

# Parse the Date column as datetime objects
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Convert to datetime, set invalid dates as NaT
df = df.dropna(subset=['Date'])  # Drop rows with invalid dates

# Sort the data by Date to ensure proper plotting
df = df.sort_values(by='Date')

# Load Settings
settings_file_path = "settings.json"
with open(settings_file_path, "r") as settings_file:
    settings = json.load(settings_file)
currency = settings["Config"]["Currency"]
graph_interval = int(settings["Config"]["Graph_Interval"])  # Get the interval for x-axis ticks

# Plot the Balance vs Time
plt.figure('Balance vs Time', figsize=(10, 6))
plt.fill_between(df['Date'], df['Balance'], 0, linestyle='-', color='cornflowerblue')
plt.plot(df['Date'], df['Balance'], linestyle='-', color='navy', label='Balance')

# Format the x-axis dates to show dd/mm/yyyy
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=graph_interval))  # Use the interval from settings

# Rotate date labels for better visibility
plt.gcf().autofmt_xdate()

# Add labels, title, and grid
plt.xlabel('Date', size=13)
plt.ylabel('Balance in ' + currency, size=13, labelpad=20)  # Adjusted with label padding
plt.title('Balance Over Time', size=15)
plt.grid(True)
plt.legend()
plt.minorticks_on()
plt.ylim(0, df['Balance'].max() * 1.1)
plt.xlim(df['Date'].min(), df['Date'].max())

# Save the plot as an image
plt.savefig('budgetgraph.jpg', dpi=300, bbox_inches='tight')
# plt.show()
