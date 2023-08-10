from gurobipy import GRB, Model
from DistributionNetwork import DistributionNetwork
import os
import pdb

class CoffeeDistributionOptimizer:
    def __init__(self, network: DistributionNetwork):
        """
        Initializes the CoffeeDistributionOptimizer object.

        :param network: DistributionNetwork object containing the entire network information
        """
        self.network = network
        self.model = Model("coffee_distribution")
        self.variables = {}

    def create_variables(self):
        """
        Creates optimization variables for shipping and roasting.
        """
        for supplier, roastery in self.network.shipping_cost_from_supplier_to_roastery.keys():
            self.variables[(supplier, roastery)] = self.model.addVar(vtype=GRB.INTEGER, name=f"x_{supplier}_{roastery}")

        for roastery, cafe in self.network.shipping_cost_from_roastery_to_cafe.keys():
            for coffee_type in self.network.cafes[0].coffee_demand.keys():  # Assuming all cafes have the same coffee types
                self.variables[(roastery, cafe, coffee_type)] = self.model.addVar(vtype=GRB.INTEGER, name=f"y_{roastery}_{cafe}_{coffee_type}")

    def set_objective(self):
        """
        Sets the objective function to minimize the total cost.
        """
        shipping_cost_from_supplier = sum(
            self.variables[supplier, roastery] * self.network.get_shipping_cost_from_supplier_to_roastery(supplier, roastery)
            for supplier, roastery in self.network.shipping_cost_from_supplier_to_roastery.keys())
        
        triplets = [k for k in self.variables.keys() if len(k) == 3]

        roasting_and_shipping_cost_to_cafe = sum(
            self.variables[roastery, cafe, coffee_type] * (roastery_obj.get_roasting_cost(coffee_type) +
                                                           self.network.get_shipping_cost_from_roastery_to_cafe(roastery, cafe))
            #for roastery, cafe, coffee_type in self.variables.keys()
            for roastery, cafe, coffee_type in triplets
            if (roastery, cafe) in self.network.shipping_cost_from_roastery_to_cafe.keys()
            for roastery_obj in self.network.roasteries if roastery_obj.name == roastery)

        self.model.setObjective(shipping_cost_from_supplier + roasting_and_shipping_cost_to_cafe, GRB.MINIMIZE)

    def add_constraints(self):
        """
        Adds constraints for flow conservation, supply, demand, and specific roasting constraints.
        """
        # Conservation of flow constraints
        for roastery in self.network.roasteries:
            incoming_flow = sum(self.variables[supplier.name, roastery.name] for supplier in self.network.suppliers)
            outgoing_flow = sum(self.variables[roastery.name, cafe.name, coffee_type] for cafe in self.network.cafes
                                for coffee_type in cafe.coffee_demand.keys())
            self.model.addConstr(incoming_flow == outgoing_flow, f"flow_{roastery.name}")

        # Supply constraints
        for supplier in self.network.suppliers:
            outgoing_flow = sum(self.variables[supplier.name, roastery.name] for roastery in self.network.roasteries)
            self.model.addConstr(outgoing_flow <= supplier.capacity, f"supply_{supplier.name}")

        # Demand constraints
        for cafe in self.network.cafes:
            for coffee_type, quantity in cafe.coffee_demand.items():
                incoming_flow = sum(self.variables[roastery.name, cafe.name, coffee_type] for roastery in self.network.roasteries)
                self.model.addConstr(incoming_flow >= quantity, f"demand_{cafe.name}_{coffee_type}")


        # TODO: double check these constraints
        # Roasting constraints (e.g., specific roasting methods for certain bean types)
        for roastery in self.network.roasteries:
            for coffee_type in self.network.cafes[0].coffee_demand.keys():  # Assuming all cafes have the same coffee types
                if not roastery.validate_roasting_constraints(coffee_type, roastery.get_roasting_constraints(coffee_type)):
                    self.model.addConstr(sum(self.variables[roastery.name, cafe.name, coffee_type] for cafe in self.network.cafes) == 0,
                                         f"roasting_constraint_{roastery.name}_{coffee_type}")
                    

        for supplier in self.network.suppliers:
            if supplier.location.lower() == "vietnam":
                self.add_cold_brew_constraint(supplier.name)


    def add_cold_brew_constraint(self, vietnam_supplier_name: str):
        """
        Adds a constraint that "cold brew coffee" should only use coffee beans from a supplier named "Vietnam."

        :param vietnam_supplier_name: Name of the supplier from Vietnam
        """
        # Get the variable for "cold brew" coffee from the supplier "Vietnam"
        cold_brew_var_from_vietnam = self.variables.get((vietnam_supplier_name, "Cold Brew"), None)

        # If the variable is not found, the constraint cannot be added
        if cold_brew_var_from_vietnam is None:
            print(f"Error: No cold brew variable found for supplier {vietnam_supplier_name}")
            return

        # Sum of all cold brew variables except the one from "Vietnam"
        other_cold_brew_vars = sum(var for (supplier, coffee_type), var in self.variables.items()
                                   if coffee_type == "Cold Brew" and supplier != vietnam_supplier_name)

        # Add constraint that the sum of other cold brew variables must be zero
        self.model.addConstr(other_cold_brew_vars == 0, "cold_brew_constraint")


    def add_customized_constraint(self, constraint):
        """
        Adds a customized constraint to the optimization model.

        :param constraint: A Gurobi constraint expression
        """
        self.model.addConstr(constraint)

    def optimize(self):
        """
        Optimizes the model and prints the results.
        """
        self.model.optimize()
        if self.model.status == GRB.OPTIMAL:
            print(f'Optimal cost: {self.model.objVal}')
        else:
            print("Not solved to optimality. Optimization status:", self.model.status)

    def run(self):
        """
        Runs the optimization process.
        """
        self.create_variables()
        self.set_objective()
        self.add_constraints()
        self.optimize()


    def log_solution(self, output_file: str, header: str=""):
        """
        Logs the optimal solution by printing the values of the decision variables.
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        f = open(output_file, "w", encoding="utf-8")
        f.write(header + "\n")
        if self.model.status != GRB.OPTIMAL:
            f.write("No optimal solution found. Cannot log the solution.")
            return

        print("\nOptimal Solution:")
        for var in self.model.getVars():
            if var.x != 0:  # Only print non-zero variables
                f.write(f"{var.varName}: {var.x}\n")
        f.close()
