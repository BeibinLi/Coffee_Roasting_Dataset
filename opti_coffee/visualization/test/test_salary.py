import pytest
import pandas as pd
import matplotlib.pyplot as plt
import os
from salary import plot

def test_plot():
    # Create a sample DataFrame with salary data
    data = pd.DataFrame({
        'employee_id': [1, 2, 3, 4, 5],
        'salary': [50000, 60000, 70000, 80000, 90000]
    })
    salary_quantum = 10000

    # Test the plot function with the sample DataFrame
    plot(data, salary_quantum)

    # Check that the image file was created
    assert os.path.exists("images/salary.png")