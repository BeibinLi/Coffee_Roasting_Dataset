from supplier import Supplier
from roastery import Roastery
from cafe import Cafe
from DistributionNetwork import DistributionNetwork
from CoffeeDistributionOptimizer import CoffeeDistributionOptimizer

# Define Suppliers
supplier1 = Supplier(name="Supplier1", capacity=1000, location="Brazil", contact="info@supplier1.com")
supplier2 = Supplier(name="Supplier2", capacity=1500, location="Colombia", contact="info@supplier2.com")

# Define Roasteries
roastery1 = Roastery(name="Roastery1", location="New York", contact="info@roastery1.com")
roastery1.set_roasting_cost("Espresso", 5)
roastery1.set_roasting_cost("Cold Brew", 4, constraints="Robusta beans only")
roastery2 = Roastery(name="Roastery2", location="Chicago", contact="info@roastery2.com")
roastery2.set_roasting_cost("Espresso", 6)
roastery2.set_roasting_cost("Cold Brew", 3)

# Define Cafes
cafe1 = Cafe(name="Cafe1", location="Boston", contact="info@cafe1.com")
cafe1.set_coffee_demand("Espresso", 200)
cafe1.set_coffee_demand("Cold Brew", 150)
cafe2 = Cafe(name="Cafe2", location="Seattle", contact="info@cafe2.com")
cafe2.set_coffee_demand("Espresso", 300)
cafe2.set_coffee_demand("Cold Brew", 100)

# Create Distribution Network
network = DistributionNetwork()
network.add_supplier(supplier1)
network.add_supplier(supplier2)
network.add_roastery(roastery1)
network.add_roastery(roastery2)
network.add_cafe(cafe1)
network.add_cafe(cafe2)

# Set shipping costs
network.set_shipping_cost_from_supplier_to_roastery(supplier1, roastery1, 10)
network.set_shipping_cost_from_supplier_to_roastery(supplier1, roastery2, 12)
network.set_shipping_cost_from_supplier_to_roastery(supplier2, roastery1, 8)
network.set_shipping_cost_from_supplier_to_roastery(supplier2, roastery2, 11)
network.set_shipping_cost_from_roastery_to_cafe(roastery1, cafe1, 6)
network.set_shipping_cost_from_roastery_to_cafe(roastery1, cafe2, 7)
network.set_shipping_cost_from_roastery_to_cafe(roastery2, cafe1, 5)
network.set_shipping_cost_from_roastery_to_cafe(roastery2, cafe2, 4)

# Create and run the optimizer
optimizer = CoffeeDistributionOptimizer(network)
optimizer.run()
