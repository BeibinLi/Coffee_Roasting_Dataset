#include <iostream>
#include <sstream>
#include "Supplier.h"
#include "catch.hpp"

TEST_CASE("Test Supplier initialization") {
    Supplier supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
    REQUIRE(supplier.get_name() == "Coffee Bean Co.");
    REQUIRE(supplier.get_capacity() == 1000);
    REQUIRE(supplier.get_location() == "Seattle");
    REQUIRE(supplier.get_contact() == "123-456-7890");
    REQUIRE(supplier.get_shipping_costs().empty());
}

TEST_CASE("Test set_shipping_cost") {
    Supplier supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
    supplier.set_shipping_cost("Roastery A", 50);
    REQUIRE(supplier.get_shipping_costs()["Roastery A"] == 50);
}

TEST_CASE("Test get_shipping_cost") {
    Supplier supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
    supplier.set_shipping_cost("Roastery A", 50);
    REQUIRE(supplier.get_shipping_cost("Roastery A") == 50);
    REQUIRE(supplier.get_shipping_cost("Roastery B") == std::numeric_limits<double>::infinity());
}

TEST_CASE("Test Supplier to string") {
    Supplier supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
    REQUIRE(supplier.to_string() == "Supplier(name=Coffee Bean Co., capacity=1000, location=Seattle, contact=123-456-7890)");
}

TEST_CASE("Test validate_capacity") {
    Supplier supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
    REQUIRE(supplier.validate_capacity(500) == true);
    REQUIRE(supplier.validate_capacity(1500) == false);
}