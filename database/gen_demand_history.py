import random
import csv
import numpy as np

def generate_demand_price_history_csv(file_name, num_cafe=100, 
                                      number_of_products=35, years=5):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['customer_id', 'product_id', 'month', 'year', 'quantity'])
        # Write the data rows
        for cafe_id in range(num_cafe):
            for product_id in range(number_of_products):
                for year in range(years):
                    for month in range(12):
                        quantity = np.random.randint(10, 500) # Random quantity between 10 and 500
                        writer.writerow([cafe_id, product_id, month + 1, year + 1, quantity])

random.seed(3)
np.random.seed(3)
file_name = 'demand_history.csv'
generate_demand_price_history_csv(file_name, num_cafe=100, number_of_products=35, years=10)
print(f'{file_name} has been created with simulated sell price history data.')
