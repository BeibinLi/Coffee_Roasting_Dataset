import pandas as pd
import matplotlib.pyplot as plt

# Load the customer data
df = pd.read_csv('../database/customer.csv')

# Convert 'member_since' column to datetime format
df['member_since'] = pd.to_datetime(df['member_since'])

# Extract the year and month from the 'member_since' column
df['membership_year_month'] = df['member_since'].dt.to_period('M')

# Count the number of members who joined each month and year
membership_counts = df['membership_year_month'].value_counts().sort_index()

# Plotting
plt.figure(figsize=(15,7))
membership_counts.plot(kind='bar', color='skyblue')
plt.title('Duration of Membership (Monthly)')
plt.xlabel('Year-Month')
plt.ylabel('Number of Customers Joined')
plt.xticks(rotation=45)
plt.tight_layout()

os.makedirs('../images', exist_ok=True)
plt.savefig('../images/membership_duration.png')
