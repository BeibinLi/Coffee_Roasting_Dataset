import random
import json
import csv
from faker import Faker
import pycountry
from country_code_to_locale import country_code_to_locale
from constant import customer_sites

file_name = "customer.csv"
random.seed(23)


payment_type = ["credit", "debit", "cash"]
roast_type = ["light", "dark"]
subscription_type = ["weekly", "monthly", "yearly"]
bean_type = ["arabica", "robusta", "liberica", "excelsa"]

used_names = set()

default_fake = Faker("en")

with open(file_name, 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['cafe_name', 'contact_name', 'open_date', 'member_since',
                    'phone_number', 'address', 'city', 'country',
                    'email', 'fav_payment_type',  'fav_subscription_type'])

    for site in customer_sites:
        country = pycountry.countries.search_fuzzy(site['country'])[0]
        locale = country_code_to_locale[country.alpha_2]
        try:
            fake = Faker(locale)
        except:
            # locale config not supported
            try:
                fake = Faker(locale[:2])
            except:
                fake = default_fake
        for _ in range(1):
            name = ""
            while True:
                name = fake.name()
                if name not in used_names:
                    used_names.add(name)
                    break
            dob = fake.date_of_birth(minimum_age=10, maximum_age=50)
            member_since = fake.date_this_decade(before_today=True, after_today=False)
            try:
                phone_number = fake.phone_number()
            except:
                phone_number = default_fake.phone_number()
            address = fake.street_address()
            email = fake.email()
            fav_payment_type = random.choice(payment_type)
            fav_subscription_type = random.choice(subscription_type)

            writer.writerow([
                site["name"], name, dob, member_since,
                phone_number,
                address, site['city'], site['country'],
                email,
                fav_payment_type,
                fav_subscription_type,
            ])



#%% On the way, generate customer order history