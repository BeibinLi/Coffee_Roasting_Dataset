class Roastery:
    def __init__(self, name: str, location: str, contact: str):
        """
        Initializes a Roastery object.

        :param name: Name of the roastery
        :param location: Location of the roastery
        :param contact: Contact information of the roastery
        """
        self.name = name
        self.location = location
        self.contact = contact
        self.roasting_costs = {}  # Costs for roasting different coffee types
        self.shipping_costs = {}  # Costs to different cafes

    def set_roasting_cost(self, coffee_type: str, cost: int, constraints=None):
        """
        Sets the roasting cost for a specific coffee type.

        :param coffee_type: Type of coffee (e.g., "Cold Brew", "Espresso")
        :param cost: Roasting cost
        :param constraints: Specific constraints for roasting (e.g., "Robusta beans only")
        """
        self.roasting_costs[coffee_type] = {'cost': cost, 'constraints': constraints}

    def set_shipping_cost(self, cafe_name: str, cost: int):
        """
        Sets the shipping cost to a specific cafe.

        :param cafe_name: Name of the cafe
        :param cost: Shipping cost
        """
        self.shipping_costs[cafe_name] = cost

    def get_shipping_cost(self, cafe_name: str) -> int:
        """
        Gets the shipping cost to a specific cafe.

        :param cafe_name: Name of the cafe
        :return: Shipping cost
        """
        return self.shipping_costs.get(cafe_name, float('inf'))

    def get_roasting_cost(self, coffee_type: str) -> int:
        """
        Gets the roasting cost for a specific coffee type.

        :param coffee_type: Type of coffee
        :return: Roasting cost
        """
        return self.roasting_costs.get(coffee_type, {}).get('cost', float('inf'))

    def get_roasting_constraints(self, coffee_type: str) -> str:
        """
        Gets the roasting constraints for a specific coffee type.

        :param coffee_type: Type of coffee
        :return: Roasting constraints
        """
        return self.roasting_costs.get(coffee_type, {}).get('constraints', None)

    def display_info(self):
        """
        Displays information about the roastery.
        """
        print(f"Name: {self.name}")
        print(f"Location: {self.location}")
        print(f"Contact: {self.contact}")
        print("Roasting Costs:")
        for coffee_type, details in self.roasting_costs.items():
            print(f"  - {coffee_type}: {details['cost']} (Constraints: {details['constraints']})")
        print("Shipping Costs:")
        for cafe, cost in self.shipping_costs.items():
            print(f"  - {cafe}: {cost}")

    def validate_roasting_constraints(self, coffee_type: str, constraints: str) -> bool:
        """
        Validates if the given constraints match the roasting constraints for the specified coffee type.

        :param coffee_type: Type of coffee
        :param constraints: Constraints to validate
        :return: True if valid, False otherwise
        """
        required_constraints = self.get_roasting_constraints(coffee_type)
        return required_constraints is None or required_constraints == constraints

    def __str__(self) -> str:
        """
        String representation of the Roastery object.

        :return: String representation
        """
        return f"Roastery(name={self.name}, location={self.location}, contact={self.contact})"

    def __repr__(self) -> str:
        """
        Formal string representation of the Roastery object.

        :return: Formal string representation
        """
        return self.__str__()
