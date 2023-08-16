import pytest
from distribution_network import DistributionNetwork
from plan_optimizer import CoffeeDistributionOptimizer

def test_create_variables():
    network = DistributionNetwork()
    optimizer = CoffeeDistributionOptimizer(network)
    optimizer.create_variables()
    assert len(optimizer.variables) == 12  # Assuming 2 suppliers, 2 roasteries, and 2 cafes

def test_set_objective():
    network = DistributionNetwork()
    optimizer = CoffeeDistributionOptimizer(network)
    optimizer.create_variables()
    optimizer.set_objective()
    assert optimizer.model.getObjective().getSense() == GRB.MINIMIZE

def test_add_constraints():
    network = DistributionNetwork()
    optimizer = CoffeeDistributionOptimizer(network)
    optimizer.create_variables()
    optimizer.set_objective()
    optimizer.add_constraints()
    assert len(optimizer.model.getConstrs()) == 12  # Assuming 2 suppliers, 2 roasteries, and 2 cafes