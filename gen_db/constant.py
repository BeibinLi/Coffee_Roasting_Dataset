import json
import random

customer_sites =  []
with open("customer_names.json", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        customer_sites.append(data)


roastery_sites = []
with open("roastery_countries.json", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        roastery_sites.append(data)



num_cafes = len(customer_sites)
num_roasteries = len(roastery_sites)

num_products = 33
num_suppliers = 50
num_years = 10
last_year = 2024

random.seed(100) # in case we forgot to set seed in the main code.
