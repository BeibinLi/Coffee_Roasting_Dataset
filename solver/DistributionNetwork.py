from supplier import Supplier
from roastery import Roastery
from cafe import Cafe

class DistributionNetwork:
    def __init__(self):
        """
        Initializes the DistributionNetwork object.
        """
        self.suppliers = []
        self.roasteries = []
        self.cafes = []
        self.shipping_cost_from_supplier_to_roastery = {}
        self.shipping_cost_from_roastery_to_cafe = {}

    def add_supplier(self, supplier: Supplier):
        """
        Adds a supplier to the network.

        :param supplier: Supplier object
        """
        self.suppliers.append(supplier)

    def add_roastery(self, roastery: Roastery):
        """
        Adds a roastery to the network.

        :param roastery: Roastery object
        """
        self.roasteries.append(roastery)

    def add_cafe(self, cafe: Cafe):
        """
        Adds a cafe to the network.

        :param cafe: Cafe object
        """
        self.cafes.append(cafe)

    def set_shipping_cost_from_supplier_to_roastery(self, supplier: Supplier, roastery: Roastery, cost: int):
        """
        Sets the shipping cost from a supplier to a roastery.

        :param supplier: Supplier object
        :param roastery: Roastery object
        :param cost: Shipping cost
        """
        self.shipping_cost_from_supplier_to_roastery[(supplier.name, roastery.name)] = cost

    def set_shipping_cost_from_roastery_to_cafe(self, roastery: Roastery, cafe: Cafe, cost: int):
        """
        Sets the shipping cost from a roastery to a cafe.

        :param roastery: Roastery object
        :param cafe: Cafe object
        :param cost: Shipping cost
        """
        self.shipping_cost_from_roastery_to_cafe[(roastery.name, cafe.name)] = cost

    def get_shipping_cost_from_supplier_to_roastery(self, supplier_name: str, roastery_name: str) -> int:
        """
        Gets the shipping cost from a supplier to a roastery.

        :param supplier_name: Name of the supplier
        :param roastery_name: Name of the roastery
        :return: Shipping cost
        """
        return self.shipping_cost_from_supplier_to_roastery.get((supplier_name, roastery_name), float('inf'))

    def get_shipping_cost_from_roastery_to_cafe(self, roastery_name: str, cafe_name: str) -> int:
        """
        Gets the shipping cost from a roastery to a cafe.

        :param roastery_name: Name of the roastery
        :param cafe_name: Name of the cafe
        :return: Shipping cost
        """
        return self.shipping_cost_from_roastery_to_cafe.get((roastery_name, cafe_name), float('inf'))

    def display_network_info(self):
        """
        Displays information about the entire distribution network.
        """
        print("Suppliers:")
        for supplier in self.suppliers:
            print(supplier)
        print("\nRoasteries:")
        for roastery in self.roasteries:
            print(roastery)
        print("\nCafes:")
        for cafe in self.cafes:
            print(cafe)
