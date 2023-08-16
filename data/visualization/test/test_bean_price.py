import pytest
import pandas as pd
from bean_price import plot_data
import os

def test_plot_data():
    data = pd.DataFrame({
        'date': ['2021-01-01', '2021-01-02', '2021-01-03'],
        'min': [5, 6, 7],
        'max': [10, 12, 14],
        'mean': [7.5, 9, 10.5]
    })
    bean_name = 'arabica'
    plot_data(data, bean_name)

    # Check that the image file was created
    assert os.path.exists(f"images/bean_price_{bean_name}.png")