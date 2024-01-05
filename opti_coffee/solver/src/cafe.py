class Cafe:
    def __init__(self, name: str, location: str, contact: str):
        """
        Initializes a Cafe object.

        :param name: Name of the cafe
        :param location: Location of the cafe
        :param contact: Contact information of the cafe
        """
        self.name = name
        self.location = location
        self.contact = contact
        self.coffee_demand = {}  # Demand for different coffee types

    def set_coffee_demand(self, coffee_type: str, quantity: int):
        """
        Sets the demand for a specific coffee type.

        :param coffee_type: Type of coffee (e.g., "Cold Brew", "Espresso")
        :param quantity: Quantity of coffee needed
        """
        self.coffee_demand[coffee_type] = quantity

    def get_coffee_demand(self, coffee_type: str) -> int:
        """
        Gets the demand for a specific coffee type.

        :param coffee_type: Type of coffee
        :return: Quantity of coffee needed
        """
        return self.coffee_demand.get(coffee_type, 0)

    def display_info(self):
        """
        Displays information about the cafe.
        """
        print(f"Name: {self.name}")
        print(f"Location: {self.location}")
        print(f"Contact: {self.contact}")
        print("Coffee Demand:")
        for coffee_type, quantity in self.coffee_demand.items():
            print(f"  - {coffee_type}: {quantity}")

    def __str__(self) -> str:
        """
        String representation of the Cafe object.

        :return: String representation
        """
        return f"Cafe(name={self.name}, location={self.location}, contact={self.contact})"

    def __repr__(self) -> str:
        """
        Formal string representation of the Cafe object.

        :return: Formal string representation
        """
        return self.__str__()

    def fulfill_demand(self, coffee_type: str, quantity: int):
        """
        Reduces the demand for a specific coffee type by the fulfilled quantity.

        :param coffee_type: Type of coffee
        :param quantity: Quantity of coffee fulfilled
        """
        current_demand = self.get_coffee_demand(coffee_type)
        if quantity > current_demand:
            raise ValueError("Fulfilled quantity exceeds demand")
        self.coffee_demand[coffee_type] = current_demand - quantity
