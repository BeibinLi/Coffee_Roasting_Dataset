#include <iostream>
#include <sstream>
#include "Roastery.h"
#include "catch.hpp"

TEST_CASE("Test Roastery initialization") {
    Roastery roastery("Blue Bottle", "San Francisco", "123-456-7890");
    REQUIRE(roastery.get_name() == "Blue Bottle");
    REQUIRE(roastery.get_location() == "San Francisco");
    REQUIRE(roastery.get_contact() == "123-456-7890");
    REQUIRE(roastery.get_roasting_costs().empty());
    REQUIRE(roastery.get_shipping_costs().empty());
}

TEST_CASE("Test set_roasting_cost") {
    Roastery roastery("Blue Bottle", "San Francisco", "123-456-7890");
    roastery.set_roasting_cost("Cold Brew", 50, "Robusta beans only");
    REQUIRE(roastery.get_roasting_costs()["Cold Brew"].cost == 50);
    REQUIRE(roastery.get_roasting_costs()["Cold Brew"].constraints == "Robusta beans only");
}

TEST_CASE("Test set_shipping_cost") {
    Roastery roastery("Blue Bottle", "San Francisco", "123-456-7890");
    roastery.set_shipping_cost("Starbucks", 100);
    REQUIRE(roastery.get_shipping_costs()["Starbucks"] == 100);
}

TEST_CASE("Test get_shipping_cost") {
    Roastery roastery("Blue Bottle", "San Francisco", "123-456-7890");
    roastery.set_shipping_cost("Starbucks", 100);
    REQUIRE(roastery.get_shipping_cost("Starbucks") == 100);
    REQUIRE(roastery.get_shipping_cost("Peet's Coffee") == std::numeric_limits<double>::infinity());
}

TEST_CASE("Test get_roasting_cost") {
    Roastery roastery("Blue Bottle", "San Francisco", "123-456-7890");
    roastery.set_roasting_cost("Cold Brew", 50, "Robusta beans only");
    REQUIRE(roastery.get_roasting_cost("Cold Brew") == 50);
    REQUIRE(roastery.get_roasting_cost("Espresso") == std::numeric_limits<double>::infinity());
}