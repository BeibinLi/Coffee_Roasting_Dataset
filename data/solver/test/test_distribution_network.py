import pytest
from distribution_network import DistributionNetwork
from supplier import Supplier
from roastery import Roastery
from cafe import Cafe

def test_add_supplier():
    network = DistributionNetwork()
    supplier = Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890")
    network.add_supplier(supplier)
    assert len(network.suppliers) == 1
    assert network.suppliers[0] == supplier

def test_add_roastery():
    network = DistributionNetwork()
    roastery = Roastery("Blue Bottle", "San Francisco", "123-456-7890")
    network.add_roastery(roastery)
    assert len(network.roasteries) == 1
    assert network.roasteries[0] == roastery

def test_add_cafe():
    network = DistributionNetwork()
    cafe = Cafe("Starbucks", "New York", "123-456-7890")
    network.add_cafe(cafe)
    assert len(network.cafes) == 1
    assert network.cafes[0] == cafe

def test_set_shipping_cost_from_supplier_to_roastery():
    network = DistributionNetwork()
    supplier = Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890")
    roastery = Roastery("Blue Bottle", "San Francisco", "123-456-7890")
    network.add_supplier(supplier)
    network.add_roastery(roastery)
    network.set_shipping_cost_from_supplier_to_roastery(supplier, roastery, 50)
    assert network.shipping_cost_from_supplier_to_roastery == {("Coffee Bean Co.", "Blue Bottle"): 50}

def test_set_shipping_cost_from_roastery_to_cafe():
    network = DistributionNetwork()
    roastery = Roastery("Blue Bottle", "San Francisco", "123-456-7890")
    cafe = Cafe("Starbucks", "New York", "123-456-7890")
    network.add_roastery(roastery)
    network.add_cafe(cafe)
    network.set_shipping_cost_from_roastery_to_cafe(roastery, cafe, 100)
    assert network.shipping_cost_from_roastery_to_cafe == {("Blue Bottle", "Starbucks"): 100}