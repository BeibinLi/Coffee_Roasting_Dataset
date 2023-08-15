import pandas as pd
import matplotlib.pyplot as plt
import os

def plot(df, salary_quantum):
    min_salary = df['salary'].min() // salary_quantum * salary_quantum
    max_salary = (df['salary'].max() + salary_quantum - 1) // salary_quantum * salary_quantum
    bins = range(min_salary, max_salary + salary_quantum, salary_quantum)

    # Plot the bar chart
    plt.hist(df['salary'], bins=bins, color='skyblue', edgecolor='black', alpha=0.7)

    plt.title('Distribution of Salaries')
    plt.xlabel('Salary Amount')
    plt.ylabel('Frequency')
    plt.grid(axis='y')

    # Display the plot
    plt.tight_layout()
    #plt.show()

    os.makedirs('images', exist_ok=True)
    plt.savefig('images/salary.png')

if __name__ == "__main__":
    df = pd.read_csv('database/employee.csv')
    plot(df, 1000)
