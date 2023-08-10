import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

parser = argparse.ArgumentParser(description='Plot the range of bean price for a specified bean.')
parser.add_argument('--name', type=str, default=None, required=True, help='Bean Name, for example Arabica')
args = parser.parse_args()

# Read the sell_price_history.csv data
df = pd.read_csv('database/sell_price_history.csv')

bean_name = args.name.lower()
filtered_data = df[df['source_bean_type'].str.lower() == bean_name]

if filtered_data.shape[0] == 0:
    raise ValueError(f'No bean with name {args.name} found.')

# Convert the month and year columns to a single datetime column
filtered_data['date'] = pd.to_datetime(filtered_data['year'].astype(str) + '-' + filtered_data['month'].astype(str) + '-01')

# Group by the date and calculate min, max, and mean
grouped_data = filtered_data.groupby('date')['price_per_unit'].agg(['min', 'max', 'mean']).reset_index()

# Plot
plt.figure(figsize=(12, 6))

# Fill the region between min and max
plt.fill_between(grouped_data['date'], grouped_data['min'], grouped_data['max'], color='skyblue', alpha=0.4, label='Price Range (Min to Max)')

# Plot mean price
plt.plot(grouped_data['date'], grouped_data['mean'], color='blue', marker='o', label='Mean Price')

plt.title(f'Bean Price Chart for {bean_name}')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.tight_layout()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

os.makedirs('images', exist_ok=True)
plt.savefig(f"images/bean_price_{bean_name}.png")