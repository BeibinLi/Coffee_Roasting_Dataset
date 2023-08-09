import csv
import pandas as pd
import glob
import os
import random
import json
from faker import Faker
import pycountry
from country_code_to_locale import country_code_to_locale
import numpy as np
from scipy.stats import norm
import pdb

files = glob.glob("*")
assert "customer.csv" in files, "Please run database/gen_customer.py first"
assert "supplier.csv" in files, "Please run database/gen_supplier.py first"
assert "sell_price_history.csv" in files, "Please run database/gen_sales_price_history.py first"

supply = pd.read_csv("supplier.csv")
customer = pd.read_csv("customer.csv")
price = pd.read_csv("sell_price_history.csv")

# Path to the generated CSV file
csv_file_path = 'roastery.csv'

# Number of roasteries to generate
random.seed(10)

n_product = price["roasting_id"].nunique()

# Header for the CSV file
header = [
    "Roastery ID",
    "City",
    "Country",
    "Contact Email"
] + [f"ship_cost_supply_{i+1}" for i in range(supply.shape[0])] + [
    f"ship_cost_customer_{i+1}" for i in range(customer.shape[0])] + [
        f"roast_cost_product_{i+1}" for i in range(n_product)] 

def random_shipping_cost(src_country: str, dest_country: str):
    # pdb.set_trace()
    if src_country.lower() == dest_country.lower():
        rst = random.uniform(0.5, 2.5)
    else:
        rst = random.uniform(2, 5.0)
    return round(rst, 2)


def random_roast_cost(roast_id: int):
    roast_info = price[price["roasting_id"] == roast_id]

    # roasting_methods = {'Light': 0.3, 'Medium': 0.3, 'Dark': 0.3, 'Cold Brew': 0.1}
    # source_bean_countries = ['Brazil', 'Colombia', 'Indonesia', 'Ethiopia',  'Vietnam', 'China']
    # source_bean_types = {'Arabica': 0.7, 'Robusta':0.2, 'Liberica':0.05, 'Excelsa':0.05}
    bean = roast_info["source_bean_type"].iloc[0]
    method = roast_info["roasting_method"].iloc[0]

    cost = 0
    if bean == "Arabica":
        cost += 0.7
    elif bean == "Robusta":
        cost += 0.2
    elif bean == "Liberica":
        cost += 0.15
    else:
        cost += 0.1

    if method == "Light":
        cost += 0.15
    elif method == "Medium":
        cost += 0.2
    elif method == "Dark":
        cost += 0.3
    else:
        cost += 0.1
    
    cost += np.random.normal(0, 0.05)
    return round(cost, 2)
    
# Roasting Sites:
sites = []
with open("roastery_countries.json", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        sites.append(data)

# Sample data for the CSV file
rows = []
for i, site in enumerate(sites):
    country_obj = pycountry.countries.search_fuzzy(site['country'])[0]
    locale = country_code_to_locale[country_obj.alpha_2]

    try:
        fake = Faker(locale)
    except:
        # locale config not supported
        try:
            fake = Faker(locale[:2])
        except:
            fake = Faker("en")

    row = [
        f"{i+1}",
        site['city'], site['country'],
        f"contact@roastery{i+1}.com",
    ] 
    
    # shipping cost from supplier
    row += [random_shipping_cost(_country, site["country"]) for _country in supply.country]

    # shipping cost to customer
    row += [random_shipping_cost(_country, site["country"]) for _country in customer.country]

    # Roasting operation cost
    row += [random_roast_cost(product_id) for product_id in price["roasting_id"].unique()]

    rows.append(row)

# Writing the CSV file
with open(csv_file_path, mode='w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(rows)


