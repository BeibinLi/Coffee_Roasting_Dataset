#include <iostream>
#include <sstream>
#include "Cafe.h"
#include "catch.hpp"

TEST_CASE("Test Cafe initialization") {
    Cafe cafe("Starbucks", "New York", "123-456-7890");
    REQUIRE(cafe.get_name() == "Starbucks");
    REQUIRE(cafe.get_location() == "New York");
    REQUIRE(cafe.get_contact() == "123-456-7890");
    REQUIRE(cafe.get_coffee_demand().empty());
}

TEST_CASE("Test set_coffee_demand") {
    Cafe cafe("Starbucks", "New York", "123-456-7890");
    cafe.set_coffee_demand("Cold Brew", 10);
    REQUIRE(cafe.get_coffee_demand()["Cold Brew"] == 10);
}

TEST_CASE("Test get_coffee_demand") {
    Cafe cafe("Starbucks", "New York", "123-456-7890");
    cafe.set_coffee_demand("Cold Brew", 10);
    REQUIRE(cafe.get_coffee_demand("Cold Brew") == 10);
    REQUIRE(cafe.get_coffee_demand("Espresso") == 0);
}

TEST_CASE("Test display_info") {
    Cafe cafe("Starbucks", "New York", "123-456-7890");
    cafe.set_coffee_demand("Cold Brew", 10);
    std::stringstream buffer;
    std::streambuf* old = std::cout.rdbuf(buffer.rdbuf());
    cafe.display_info();
    std::string output = buffer.str();
    std::cout.rdbuf(old);
    REQUIRE(output == "Name: Starbucks\nLocation: New York\nContact: 123-456-7890\nCoffee Demand:\n  - Cold Brew: 10\n");
}

TEST_CASE("Test Cafe to string") {
    Cafe cafe("Starbucks", "New York", "123-456-7890");
    REQUIRE(cafe.to_string() == "Cafe(name=Starbucks, location=New York, contact=123-456-7890)");
}