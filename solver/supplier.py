class Supplier:
    def __init__(self, name: str, capacity: int, location: str, contact: str):
        """
        Initializes a Supplier object.

        :param name: Name of the supplier
        :param capacity: Maximum capacity of coffee beans that the supplier can provide
        :param location: Location of the supplier
        :param contact: Contact information of the supplier
        """
        self.name = name
        self.capacity = capacity
        self.location = location
        self.contact = contact
        self.shipping_costs = {}  # Costs to different roasteries

    def set_shipping_cost(self, roastery_name: str, cost: int):
        """
        Sets the shipping cost to a specific roastery.

        :param roastery_name: Name of the roastery
        :param cost: Shipping cost
        """
        self.shipping_costs[roastery_name] = cost

    def get_shipping_cost(self, roastery_name: str) -> int:
        """
        Gets the shipping cost to a specific roastery.

        :param roastery_name: Name of the roastery
        :return: Shipping cost
        """
        return self.shipping_costs.get(roastery_name, float('inf'))

    def __str__(self) -> str:
        """
        String representation of the Supplier object.

        :return: String representation
        """
        return f"Supplier(name={self.name}, capacity={self.capacity}, location={self.location}, contact={self.contact})"

    def __repr__(self) -> str:
        """
        Formal string representation of the Supplier object.

        :return: Formal string representation
        """
        return self.__str__()

    def validate_capacity(self, requested_quantity: int) -> bool:
        """
        Validates if the requested quantity is within the supplier's capacity.

        :param requested_quantity: Quantity of coffee beans requested
        :return: True if within capacity, False otherwise
        """
        return requested_quantity <= self.capacity

    def reduce_capacity(self, quantity: int):
        """
        Reduces the supplier's capacity by a specified quantity.

        :param quantity: Quantity to reduce
        """
        if self.validate_capacity(quantity):
            self.capacity -= quantity
        else:
            raise ValueError("Requested quantity exceeds capacity")

    def increase_capacity(self, quantity: int):
        """
        Increases the supplier's capacity by a specified quantity.

        :param quantity: Quantity to increase
        """
        self.capacity += quantity

    def display_info(self):
        """
        Displays information about the supplier.
        """
        print(f"Name: {self.name}")
        print(f"Capacity: {self.capacity}")
        print(f"Location: {self.location}")
        print(f"Contact: {self.contact}")
        print("Shipping Costs:")
        for roastery, cost in self.shipping_costs.items():
            print(f"  - {roastery}: {cost}")
