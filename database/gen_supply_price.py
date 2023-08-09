import csv
import math
import random
import matplotlib.pyplot as plt

def generate_price_curve(supplier_id, base_price, amplitude, frequency, phase_shift, years=5):
    prices = []
    
    inc_trend = 0
    
    for year in range(2023 - years, 2023):
        for month in range(1, 13):
            if random.random() < 0.05 or (year == 2020 and random.random() < 0.3):
                # we only raise price about every 20 months.
                # For 2020 covid year, the price is raised more often.
                # Note there are still some weird occassion when price is reduced.
                base_price += random.uniform(-0.1, 1)

            # Calculate the periodic price using a sine function
            periodic_price = base_price + amplitude * math.sin(2 * math.pi * frequency * (month + phase_shift))
            # Add random noise to the price
            final_price = periodic_price + random.uniform(-0.5, 0.5)
            # final_price = periodic_price


            final_price += inc_trend
            prices.append((supplier_id, month, year, round(final_price, 2)))
    return prices

def generate_supply_history_csv(file_name, number_of_suppliers=100, years=5):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['supplier_id', 'month', 'year', 'price_per_unit'])
        # Write the data rows
        for supplier_id in range(number_of_suppliers):
            # Generate random parameters for the price curve
            base_price = random.uniform(2.0, 5.0)
            amplitude = random.uniform(0.2, 0.5)
            frequency = random.uniform(1/36.0, 1/6.0) #  6 - 36 months
            phase_shift = random.uniform(0, 12)
            # Get the price curve for this supplier
            prices = generate_price_curve(supplier_id, base_price, amplitude, frequency, phase_shift, years)
            writer.writerows(prices)

        plt.plot(list(range(len(prices))), [price for _, _, _, price in prices])
        plt.show()


random.seed(3)
file_name = 'supply_price_history.csv'
generate_supply_history_csv(file_name, number_of_suppliers=130, years=10)
print(f'{file_name} has been created with simulated supply history price data.')
