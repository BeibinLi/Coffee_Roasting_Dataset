#include <iostream>
#include <sstream>
#include "DistributionNetwork.h"
#include "Supplier.h"
#include "Roastery.h"
#include "Cafe.h"
#include "catch.hpp"

TEST_CASE("Test add_supplier") {
    DistributionNetwork network;
    Supplier supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
    network.add_supplier(supplier);
    REQUIRE(network.get_suppliers().size() == 1);
    REQUIRE(network.get_suppliers()[0] == supplier);
}

TEST_CASE("Test add_roastery") {
    DistributionNetwork network;
    Roastery roastery("Blue Bottle", "San Francisco", "123-456-7890");
    network.add_roastery(roastery);
    REQUIRE(network.get_roasteries().size() == 1);
    REQUIRE(network.get_roasteries()[0] == roastery);
}

TEST_CASE("Test add_cafe") {
    DistributionNetwork network;
    Cafe cafe("Starbucks", "New York", "123-456-7890");
    network.add_cafe(cafe);
    REQUIRE(network.get_cafes().size() == 1);
    REQUIRE(network.get_cafes()[0] == cafe);
}

TEST_CASE("Test set_shipping_cost_from_supplier_to_roastery") {
    DistributionNetwork network;
    Supplier supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
    Roastery roastery("Blue Bottle", "San Francisco", "123-456-7890");
    network.add_supplier(supplier);
    network.add_roastery(roastery);
    network.set_shipping_cost_from_supplier_to_roastery(supplier, roastery, 50);
    REQUIRE(network.get_shipping_cost_from_supplier_to_roastery(supplier, roastery) == 50);
}

TEST_CASE("Test set_shipping_cost_from_roastery_to_cafe") {
    DistributionNetwork network;
    Roastery roastery("Blue Bottle", "San Francisco", "123-456-7890");
    Cafe cafe("Starbucks", "New York", "123-456-7890");
    network.add_roastery(roastery);
    network.add_cafe(cafe);
    network.set_shipping_cost_from_roastery_to_cafe(roastery, cafe, 100);
    REQUIRE(network.get_shipping_cost_from_roastery_to_cafe(roastery, cafe) == 100);
}