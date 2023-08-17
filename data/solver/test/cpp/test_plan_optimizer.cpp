#include <iostream>
#include <sstream>
#include "DistributionNetwork.h"
#include "CoffeeDistributionOptimizer.h"
#include "catch.hpp"

TEST_CASE("Test create_variables") {
    DistributionNetwork network;
    // Add suppliers, roasteries, and cafes to the network
    // ...

    CoffeeDistributionOptimizer optimizer(network);
    optimizer.create_variables();
    REQUIRE(optimizer.get_variables().size() == 12);  // Assuming 2 suppliers, 2 roasteries, and 2 cafes
}

TEST_CASE("Test set_objective") {
    DistributionNetwork network;
    // Add suppliers, roasteries, and cafes to the network
    // ...

    CoffeeDistributionOptimizer optimizer(network);
    optimizer.create_variables();
    optimizer.set_objective();
    REQUIRE(optimizer.get_model().get(GRB_IntAttr_ModelSense) == GRB_MINIMIZE);
}

TEST_CASE("Test add_constraints") {
    DistributionNetwork network;
    // Add suppliers, roasteries, and cafes to the network
    // ...

    CoffeeDistributionOptimizer optimizer(network);
    optimizer.create_variables();
    optimizer.set_objective();
    optimizer.add_constraints();
    REQUIRE(optimizer.get_model().get(GRB_IntAttr_NumConstrs) == 12);  // Assuming 2 suppliers, 2 roasteries, and 2 cafes
}