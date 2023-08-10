import random
import csv
import numpy as np
from constant import num_years, num_products




def generate_sell_price_history_csv(file_name, number_of_products=100, years=5):
    # Predefined values for roasting methods, source bean countries, and types
    roasting_methods = {'Light': 0.3, 'Medium': 0.3, 'Dark': 0.3, 'Cold Brew': 0.1}
    source_bean_countries = ['Brazil', 'Colombia', 'Indonesia', 'Ethiopia',  'Vietnam', 'China']
    source_bean_types = {'Arabica': 0.7, 'Robusta':0.2, 'Liberica':0.05, 'Excelsa':0.05}


    def  get_roasting_method():
        roasting_method = np.random.choice(list(roasting_methods.keys()), 
                                            p=list(roasting_methods.values()))
        source_bean_country = random.choice(source_bean_countries)
        source_bean_type = np.random.choice(list(source_bean_types.keys()), 
                                            p=list(source_bean_types.values()))

        if roasting_method == "Cold Brew":
            source_bean_country = "Vietnam"
            source_bean_type = "Robusta"
        return roasting_method, source_bean_country, source_bean_type

    added = set()
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['roasting_id', 'roasting_method', 'source_bean_country', 'source_bean_type', 'month', 'year', 'price_per_unit'])
        # Write the data rows
        for product_id in range(1, number_of_products+1):

            roasting_method, source_bean_country, source_bean_type = get_roasting_method()
            while (roasting_method, source_bean_country, source_bean_type) in added:
                roasting_method, source_bean_country, source_bean_type = get_roasting_method()
            added.add((roasting_method, source_bean_country, source_bean_type))

            curr_price = random.uniform(5.0, 15.0)
            # Increment to slightly increase the price over time
            for year in range(2023 - years, 2023):
                for month in range(1, 13):
                    # Add a slight increase to the base price and random minor fluctuations
                    
                    if random.random() < 0.05 or (year == 2020 and random.random() < 0.3):
                        # we only raise price about every 20 months.
                        # For 2020 covid year, the price is raised more often.
                        # Note there are still some weird occassion when price is reduced.
                        curr_price += random.uniform(-0.5, 2)

                    price_per_unit = curr_price
                    writer.writerow([
                        f'{product_id}',
                        roasting_method,
                        source_bean_country,
                        source_bean_type,
                        month,
                        year,
                        round(price_per_unit, 2)
                    ])

random.seed(3)
np.random.seed(3)
file_name = 'sell_price_history.csv'
generate_sell_price_history_csv(file_name, number_of_products=num_products, years=num_years)
print(f'{file_name} has been created with simulated sell price history data.')