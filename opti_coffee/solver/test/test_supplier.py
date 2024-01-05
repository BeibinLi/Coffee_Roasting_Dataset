import pytest
from supplier import Supplier

def test_supplier_init():
    supplier = Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890")
    assert supplier.name == "Coffee Bean Co."
    assert supplier.capacity == 1000
    assert supplier.location == "Seattle"
    assert supplier.contact == "123-456-7890"
    assert supplier.shipping_costs == {}

def test_set_shipping_cost():
    supplier = Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890")
    supplier.set_shipping_cost("Roastery A", 50)
    assert supplier.shipping_costs == {"Roastery A": 50}

def test_get_shipping_cost():
    supplier = Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890")
    supplier.set_shipping_cost("Roastery A", 50)
    assert supplier.get_shipping_cost("Roastery A") == 50
    assert supplier.get_shipping_cost("Roastery B") == float('inf')

def test_str():
    supplier = Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890")
    assert str(supplier) == "Supplier(name=Coffee Bean Co., capacity=1000, location=Seattle, contact=123-456-7890)"

def test_validate_capacity():
    supplier = Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890")
    assert supplier.validate_capacity(500) == True
    assert supplier.validate_capacity(1500) == False