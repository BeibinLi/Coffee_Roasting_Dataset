import csv
import os
import sqlite3

def csv_to_sql(folder_path, output_sql_file):
    # Connect to the SQLite database file
    conn = sqlite3.connect(output_sql_file)
    cursor = conn.cursor()

    # Iterate through all the CSV files in the given folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            # Define the table name based on the CSV file name
            table_name = os.path.splitext(filename)[0]

            # Read the CSV file
            with open(os.path.join(folder_path, filename), 'r', encoding="utf-8") as file:
                reader = csv.reader(file)
                columns = next(reader)  # Read the first row to get the column names
                columns = [col.replace(" ", "_") for col in columns]  # Replace spaces with underscores
                
                # Create the SQL table
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                cursor.execute(f"CREATE TABLE {table_name} ({', '.join(columns)})")

                # Insert the CSV data into the SQL table
                for row in reader:
                    cursor.execute(f"INSERT INTO {table_name} VALUES ({', '.join(['?']*len(row))})", row)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

folder_path = '.' # Replace with the path to the folder containing the CSV files
output_sql_file = 'data.sqlite'
csv_to_sql(folder_path, output_sql_file)
print(f'{output_sql_file} has been created with tables from CSV files.')
