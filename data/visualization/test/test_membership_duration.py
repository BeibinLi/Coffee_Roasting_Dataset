import pytest
import pandas as pd
from membership_duration import get_data

def test_get_data():
    # Create a sample DataFrame with membership data
    data = pd.DataFrame({
        'member_since': ['2021-01-01', '2021-01-02', '2021-02-01', '2021-02-02', '2021-03-01'],
        'customer_id': [1, 2, 3, 4, 5]
    })
    expected_output = pd.Series([2, 2, 1], index=pd.PeriodIndex(['2021-01', '2021-02', '2021-03'], freq='M'))

    # Test the get_data function with the sample DataFrame
    output = get_data(data)
    assert output.equals(expected_output)