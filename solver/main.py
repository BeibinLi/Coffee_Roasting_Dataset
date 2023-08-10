from supplier import Supplier
from roastery import Roastery
from cafe import Cafe
from DistributionNetwork import DistributionNetwork
from CoffeeDistributionOptimizer import CoffeeDistributionOptimizer
import pandas as pd
import pdb

# Read arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year", "-y", type=int, default=2023, help="Year of the simulation")
parser.add_argument("--month", "-m", type=int, default=12, help="Month of the simulation")
parser.add_argument("--base_dir", "-b", type=str, default="../database/",  help="Base directory of the database")
args = parser.parse_args()

year = args.year
month = args.month
base_dir = args.base_dir

# Read Suppliers from CSV
supplier_df = pd.read_csv(base_dir + 'supplier.csv')
supplier_map = {}
for index, row in supplier_df.iterrows():
    sid = supplier_id = row['supplier_id']
    supplier_map[sid]  = Supplier(name=row['contact_name'], 
                                  capacity=row['max_purchase_this_year'],
                              location=row['city'], contact=row['phone_number'])

# Read Demand (Cafes) from CSV
demand_history_df = pd.read_csv(base_dir + 'demand_history.csv')
product_ids = demand_history_df.product_id.unique()
demand_df = demand_history_df[(demand_history_df.year == year) & (demand_history_df.month == month)]
customer_df = pd.read_csv(base_dir + 'customer.csv')
cafe_map = {} # cafe id: cafe object


income = 0
sell_price_df = pd.read_csv(base_dir + f'sell_price_history.csv')
sprice_df = sell_price_df[(sell_price_df.year == year) & (sell_price_df.month == month)]
for index, row in demand_df.iterrows():
    customer_id = row["customer_id"]
    if customer_id not in cafe_map:
        cafe_row = customer_df[customer_df["customer_id"] == customer_id].iloc[0]
        cafe_map[customer_id] = Cafe(name=cafe_row["cafe_name"], 
                                    location=cafe_row["city"] + ", " + cafe_row["country"], 
                                    contact=cafe_row["contact_name"])
    cafe_map[customer_id].set_coffee_demand(str(row["product_id"]), 
                                            row["quantity"])
    income += sprice_df[(sprice_df.roasting_id == row["product_id"])].iloc[0]["price_per_unit"] * row["quantity"]

print(f"Total income: {income}")


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
purchase_price_df = pd.read_csv(base_dir + f'supply_price_history.csv')
price_df = purchase_price_df[(purchase_price_df.year == year) & (purchase_price_df.month == month)]
for i_r, r in roastery_map.items():
    for i_s, s in supplier_map.items():
        try:
            cost = roastery_df.loc[roastery_df["Roastery ID"] == i_r, 
                                   f"ship_cost_supply_{i_s}"].item()
            cost += price_df[price_df.supplier_id == i_s].iloc[0]["price_per_unit"]
        except:
            pdb.set_trace()
        network.set_shipping_cost_from_supplier_to_roastery(s, r, float(cost))

# Set shipping costs for roasteries to cafes
for i_r, r in roastery_map.items():
    for i_c, c in cafe_map.items():
        cost = roastery_df.loc[roastery_df["Roastery ID"] == i_r, f"ship_cost_customer_{i_c}"].item()
        network.set_shipping_cost_from_roastery_to_cafe(r, c, float(cost))

# Create and run the optimizer
optimizer = CoffeeDistributionOptimizer(network)
optimizer.run()

total_cost = optimizer.model.objVal


salary_df = pd.read_csv(base_dir + 'employee.csv') 
total_salary = salary_df["salary"].sum() / 12.0


profit = income - total_cost - total_salary

summary = f"""
--------------------------
Total Revenue: {income:.2f}
Purchasing and Shipping Cost: {total_cost:.2f}
Salary: {total_salary:.2f}
Total Profit: {profit:.2f}
--------------------------
""" 
print(summary)

optimizer.log_solution(f"output/solution_{year}_{month}.md", header=summary)

print("=" * 60)
print("\n\n")