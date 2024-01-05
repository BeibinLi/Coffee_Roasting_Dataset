import pytest
from supplier_on_map import get_coordinates

def test_get_coordinates():
    # Test the get_coordinates function with a sample city and country
    city = 'Seattle'
    country = 'USA'
    lat, lng = get_coordinates(city, country)

    # Check that the latitude and longitude are within reasonable bounds
    assert lat > 47 and lat < 48
    assert lng > -123 and lng < -122