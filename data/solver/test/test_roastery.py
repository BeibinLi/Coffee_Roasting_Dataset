import pytest
from roastery import Roastery

def test_roastery_init():
    roastery = Roastery("Blue Bottle", "San Francisco", "123-456-7890")
    assert roastery.name == "Blue Bottle"
    assert roastery.location == "San Francisco"
    assert roastery.contact == "123-456-7890"
    assert roastery.roasting_costs == {}
    assert roastery.shipping_costs == {}

def test_set_roasting_cost():
    roastery = Roastery("Blue Bottle", "San Francisco", "123-456-7890")
    roastery.set_roasting_cost("Cold Brew", 50, "Robusta beans only")
    assert roastery.roasting_costs == {"Cold Brew": {'cost': 50, 'constraints': "Robusta beans only"}}

def test_set_shipping_cost():
    roastery = Roastery("Blue Bottle", "San Francisco", "123-456-7890")
    roastery.set_shipping_cost("Starbucks", 100)
    assert roastery.shipping_costs == {"Starbucks": 100}

def test_get_shipping_cost():
    roastery = Roastery("Blue Bottle", "San Francisco", "123-456-7890")
    roastery.set_shipping_cost("Starbucks", 100)
    assert roastery.get_shipping_cost("Starbucks") == 100
    assert roastery.get_shipping_cost("Peet's Coffee") == float('inf')

def test_get_roasting_cost():
    roastery = Roastery("Blue Bottle", "San Francisco", "123-456-7890")
    roastery.set_roasting_cost("Cold Brew", 50, "Robusta beans only")
    assert roastery.get_roasting_cost("Cold Brew") == 50
    assert roastery.get_roasting_cost("Espresso") == float('inf')