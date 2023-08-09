import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

parser = argparse.ArgumentParser(description='Plot the change in supply price for a given supplier.')
parser.add_argument('--id', type=int, default=None, help='Supplier ID')
parser.add_argument('--name', type=str, default=None, help='Supplier Name')
args = parser.parse_args()

if args.id is None and args.name is None:
    raise ValueError('Either --id or --name must be specified.')

if args.id is None:
    # Get the supplier ID from the name
    suppliers = pd.read_csv('../database/suppliers.csv')
    rows = (suppliers['contact_name'] == args.name)
    
    if sum(rows) == 0:
        raise ValueError(f'No supplier with name {args.name} found.')
    elif sum(rows) > 1:
        raise ValueError(f'Multiple suppliers with name {args.name} found.')
    idx = rows.idxmax()
    supplier_id = suppliers.loc[idx, 'supplier_id']
else:
    supplier_id = args.id

# Load the data
df = pd.read_csv('../database/supply_price_history.csv')

# Filter data for the given supplier
df_filtered = df[df['supplier_id'] == supplier_id]

# Combine 'year' and 'month' columns and convert to datetime
df_filtered['date'] = pd.to_datetime(df_filtered[['year', 'month']].assign(DAY=1))

# Sort by date
df_filtered = df_filtered.sort_values(by='date')

# Plotting
plt.plot(df_filtered['date'], df_filtered['price_per_unit'], marker='o', color='b', linestyle='-')
plt.title(f'Change in Supply Price for Supplier {supplier_id}')
plt.xlabel('Date')
plt.ylabel('Price per Unit')
plt.grid(True)
plt.tight_layout()

# Show the plot
os.makedirs('../images', exist_ok=True)
plt.savefig(f'../images/supplier_price_{supplier_id}.png')
