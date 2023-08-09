import random
import json
import csv
from faker import Faker
import pycountry
from country_code_to_locale import country_code_to_locale
import numpy as np
from scipy.stats import norm
import pandas as pd

file_name = "employee.csv"

sites = []
with open("roastery_countries.json", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        sites.append(data)

positions = ['Barista', 'Manager', 'Accountant', 'Roaster', 'Cleaner', 'Cashier']
salary_ranges = {
    'Barista': (20000, 35000),
    'Manager': (30000, 90000),
    'Accountant': (45000, 100000),
    'Roaster': (30000, 60000),
    'Cleaner': (20000, 40000),
    'Cashier': (20000, 30000),
}
performance_ratings = ['Poor', 'Average', 'Good', 'Excellent']
used_names = set()

def gen_normal(lower, upper, confidence):
    mean = (lower + upper) / 2
    z_lower = norm.ppf((1 - confidence) / 2)
    z_upper = norm.ppf((1 + confidence) / 2)

    std_dev = (upper - lower) / (z_upper - z_lower) / 2

    sample = int(np.random.normal(mean, std_dev))
    return np.clip(sample, lower, upper)

with open(file_name, 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['name', 'date_of_birth', 'position', 'date_of_hire', 'salary', 'performance_rating', 'site', 'city', 'country'])

    for roastery_id, site in enumerate(sites):
        country = pycountry.countries.search_fuzzy(site['country'])[0]
        locale = country_code_to_locale[country.alpha_2]
        try:
            fake = Faker(locale)
        except:
            # locale config not supported
            try:
                fake = Faker(locale[:2])
            except:
                fake = Faker("en")
        for _ in range(random.randint(2, 10)):
            name = ""
            while True:
                name = fake.name()
                if name not in used_names:
                    used_names.add(name)
                    break
            dob = fake.date_of_birth(minimum_age=18, maximum_age=65)
            position = random.choice(positions)
            date_of_hire = fake.date_this_decade(before_today=True, after_today=False)
            salary = gen_normal(*salary_ranges[position], 0.9)
            performance_rating = random.choice(performance_ratings)

            writer.writerow([
                name, dob, position,
                date_of_hire, salary,
                performance_rating,
                roastery_id + 1,
                site['city'],
                site['country']
            ])