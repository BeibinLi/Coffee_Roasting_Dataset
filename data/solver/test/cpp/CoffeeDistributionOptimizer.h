#pragma once
#include "DistributionNetwork.h"
#include <gurobi_c++.h>

class CoffeeDistributionOptimizer {
public:
    explicit CoffeeDistributionOptimizer(const DistributionNetwork& network) : network(network) {}

    void create_variables();
    void set_objective();
    void add_constraints();
    void run();

    const GRBModel& get_model() const;
    const std::vector<GRBVar>& get_variables() const;

private:
    DistributionNetwork network;
    GRBEnv env;
    GRBModel model;
    std::vector<GRBVar> variables;
};