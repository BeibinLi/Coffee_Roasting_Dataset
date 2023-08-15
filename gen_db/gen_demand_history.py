import random
import csv
import numpy as np
import pandas as pd
from constant import num_cafes, num_years, num_products, last_year

def generate_demand_price_history_csv(file_name, num_cafe=100, 
                                      number_of_products=35, years=5):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['customer_id', 'product_id', 'month', 'year', 'quantity'])
        # Write the data rows
        for cafe_id in range(1, num_cafe + 1):
            for product_id in range(1, number_of_products + 1):
                for year in range(last_year - years, last_year):
                    for month in range(12):
                        quantity = np.random.randint(10, 500) # Random quantity between 10 and 500
                        writer.writerow([cafe_id, product_id, month + 1, year + 1, quantity])

random.seed(3)
np.random.seed(3)
file_name = 'demand_history.csv'

generate_demand_price_history_csv(file_name, num_cafe=num_cafes, 
                                  number_of_products=num_products, years=num_years)
print(f'{file_name} has been created with simulated sell price history data.')
