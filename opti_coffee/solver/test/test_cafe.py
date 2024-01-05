import pytest
from cafe import Cafe

def test_cafe_init():
    cafe = Cafe("Starbucks", "New York", "123-456-7890")
    assert cafe.name == "Starbucks"
    assert cafe.location == "New York"
    assert cafe.contact == "123-456-7890"
    assert cafe.coffee_demand == {}

def test_set_coffee_demand():
    cafe = Cafe("Starbucks", "New York", "123-456-7890")
    cafe.set_coffee_demand("Cold Brew", 10)
    assert cafe.coffee_demand == {"Cold Brew": 10}

def test_get_coffee_demand():
    cafe = Cafe("Starbucks", "New York", "123-456-7890")
    cafe.set_coffee_demand("Cold Brew", 10)
    assert cafe.get_coffee_demand("Cold Brew") == 10
    assert cafe.get_coffee_demand("Espresso") == 0

def test_display_info(capsys):
    cafe = Cafe("Starbucks", "New York", "123-456-7890")
    cafe.set_coffee_demand("Cold Brew", 10)
    cafe.display_info()
    captured = capsys.readouterr()
    assert captured.out == "Name: Starbucks\nLocation: New York\nContact: 123-456-7890\nCoffee Demand:\n  - Cold Brew: 10\n"

def test_str():
    cafe = Cafe("Starbucks", "New York", "123-456-7890")
    assert str(cafe) == "Cafe(name=Starbucks, location=New York, contact=123-456-7890)"