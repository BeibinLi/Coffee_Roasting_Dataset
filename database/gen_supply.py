import csv
import random
from faker import Faker

fake = Faker()

country_name_to_LCID = {
    "Brazil": "pt_BR",
    "Vietnam": "vi_VN",
    "Colombia": "es_CO",
    "Indonesia": "id_ID",
    "Ethiopia": "en", # not supported, use English
    "Jamaica": "en",
    "China": "zh_CN",
}

def generate_supplier_csv(file_name, number_of_records=100):
    # List of sample countries and cities
    locations = [('Vietnam', 'Hanoi'), ('Colombia', 'Bogota'), 
              ('Indonesia', 'Jakarta'), ('Ethiopia', 'Addis Ababa'), 
              ( "Jamaica", "Blue Mountains"), ("China", "Fujian"), 
              ("Brazil", "Sao Paulo"), ("Colombia", "Medellin"), ("Indonesia", "Sumatra"), 
              ("Ethiopia", "Sidamo"), ("China", "Yunnan"), ("China", "Guangdong"),
              ("Ethiopia", "Yirgacheffe"), 
              ("Indonesia", "Java"),
              ("Vietnam", "Ho Chi Minh City"), ("Colombia", "Armenia")]

    # Create and write the CSV file
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['supplier_id', 'contact_name', 'country', 'city', 'phone_number', 'address', 'max_purchase_this_year', 'unit_price', 'min_purchase_this_year'])
        # Write the data rows
        for i in range(number_of_records):

            country, city = random.choice(locations)
            LCID = country_name_to_LCID[country]
            fake = Faker(LCID)

            writer.writerow([
                str(i),
                fake.name(),
                country,
                city,
                fake.phone_number(), # phone_number
                fake.street_address(), # address
                random.randint(1000, 10000), # max_purchase_this_year
                round(random.uniform(1.5, 5.0), 2), # unit_price
                random.randint(100, 1000), # min_purchase_this_year
            ])


file_name = 'supplier.csv'

random.seed(1)
generate_supplier_csv(file_name, number_of_records=130)
print(f'{file_name} has been created with simulated supplier data.')
