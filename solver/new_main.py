from supplier import Supplier
from roastery import Roastery
from cafe import Cafe
from DistributionNetwork import DistributionNetwork
from CoffeeDistributionOptimizer import CoffeeDistributionOptimizer
import pandas as pd


year = 2023
month = 2
base_dir = "../database/"

# Read Suppliers from CSV
supplier_df = pd.read_csv(base_dir + 'supplier.csv')
supplier_map = {}
for index, row in supplier_df.iterrows():
    sid = supplier_id = row['supplier_id']
    supplier_map[sid]  = Supplier(name=row['contact_name'], capacity=row['max_purchase_this_year'],
                              location=row['city'], contact=row['phone_number'])

# Read Demand (Cafes) from CSV
demand_history_df = pd.read_csv(base_dir + 'demand_history.csv')
product_ids = demand_history_df.product_id.unique()
demand_df = demand_history_df[(demand_history_df.year == year) & (demand_history_df.month == month)]
cafe_map = {} # cafe id: cafe object
for index, row in demand_df.iterrows():
    customer_id = row["customer_id"]
    cafe_map[customer_id] = Cafe(customer_id=customer_id, location="", contact="")
    cafe_map[customer_id].set_coffee_demand(str(row["product_id"]), row["quantity"])


# Read Roasteries from CSV
roastery_df = pd.read_csv(base_dir + f'roastery_{year}.csv')
roastery_map = {}

for index, row in roastery_df.iterrows():
    rid = row['Roastery ID']
    roastery = Roastery(name=f"Roastery {rid}", contact=row['Contact Email'], location=row['City'])
    # roasting_costs = {f"product_{i + 1}": row[f'roast_cost_product_{i + 1}'] for i in range(20)}
    for pid in product_ids:
        roastery.set_roasting_cost(str(pid), row[f'roast_cost_product_{pid}'])
    roastery_map[rid] = roastery



# Creating the DistributionNetwork instance using the shipping costs
network = DistributionNetwork()


# Create Distribution Network
network = DistributionNetwork()
[network.add_supplier(s) for s in supplier_map.values()]
[network.add_roastery(r) for r in roastery_map.values()]
[network.add_cafe(c) for c in cafe_map.values()]

# Set shipping costs for suppliers to roasteries
# TODO: add supply prices from supply_price_history.csv 
for i_r, r in roastery_map.items():
    for i_s, s in supplier_map.items():
        cost = roastery_df.iloc[roastery_df["Roastery ID" == i_r], f"ship_cost_supply_{i_s}"].item()
        network.set_shipping_cost_from_supplier_to_roastery(s, r, float(cost))

# Set shipping costs for roasteries to cafes
# TODO: minus sales price from sell_price_history.csv
for i_r, r in roastery_map.items():
    for i_c, c in cafe_map.items():
        cost = roastery_df.iloc[roastery_df["Roastery ID" == i_r], f"ship_cost_customer_{i_c}"].item()
        network.set_shipping_cost_from_roastery_to_cafe(r, c, float(cost))

# Create and run the optimizer
optimizer = CoffeeDistributionOptimizer(network)
optimizer.run()
