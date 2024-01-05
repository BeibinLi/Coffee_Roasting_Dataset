import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

def get_args():
    parser = argparse.ArgumentParser(description='Plot the change in supply price for a given supplier.')
    
    parser.add_argument('--id', type=int, default=None, help='Supplier ID')
    parser.add_argument('--name', type=str, default=None, help='Supplier Name')
    
    return parser.parse_args()

def get_supplier_id(args):
    if args.id is None and args.name is None:
        raise ValueError('Either --id or --name must be specified.')

    if args.id is None:
        # Get the supplier ID from the name
        suppliers = pd.read_csv('database/supplier.csv')
        rows = (suppliers['contact_name'] == args.name)
        
        if sum(rows) == 0:
            raise ValueError(f'No supplier with name {args.name} found.')
        elif sum(rows) > 1:
            raise ValueError(f'Multiple suppliers with name {args.name} found.')
        idx = rows.idxmax()
        supplier_id = suppliers.loc[idx, 'supplier_id']
    else:
        supplier_id = args.id
    
    return supplier_id

def get_data(supplier_id):
    # Load the data
    df = pd.read_csv('database/supply_price_history.csv')

    # Filter data for the given supplier
    df_filtered = df[df['supplier_id'] == supplier_id]

    # Combine 'year' and 'month' columns and convert to datetime
    df_filtered['date'] = pd.to_datetime(df_filtered[['year', 'month']].assign(DAY=1))

    # Sort by date
    return df_filtered.sort_values(by='date')

def plot(filtered_data, supplier_id):
    # Plotting
    plt.plot(filtered_data['date'], filtered_data['price_per_unit'], marker='o', color='b', linestyle='-')
    plt.title(f'Change in Supply Price for Supplier {supplier_id}')
    plt.xlabel('Date')
    plt.ylabel('Price per Unit')
    plt.grid(True)
    plt.tight_layout()

    # Show the plot
    os.makedirs('images', exist_ok=True)
    plt.savefig(f'images/supplier_price_{supplier_id}.png')

if __name__ == '__main__':
    args = get_args()
    supplier_id = get_supplier_id(args)
    filtered_data = get_data(supplier_id)
    plot(filtered_data, supplier_id)
