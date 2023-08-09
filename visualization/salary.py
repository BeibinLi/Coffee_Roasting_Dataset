import pandas as pd
import matplotlib.pyplot as plt
import os

gap = 1000
# Read the CSV file
df = pd.read_csv('../database/employee.csv')

min_salary = df['salary'].min() // gap * gap
max_salary = (df['salary'].max() + gap - 1) // gap * gap 
bins = range(min_salary, max_salary + gap, gap)

# Calculate the frequency of each unique salary
salary_counts = df['salary'].value_counts()

# Plot the bar chart
plt.hist(df['salary'], bins=bins, color='skyblue', edgecolor='black', alpha=0.7)

plt.title('Distribution of Salaries')
plt.xlabel('Salary Amount')
plt.ylabel('Frequency')
plt.grid(axis='y')

# Display the plot
plt.tight_layout()
#plt.show()

os.makedirs('../images', exist_ok=True)
plt.savefig('../images/salary.png')
