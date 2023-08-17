#pragma once
#include "DistributionNetwork.h"
#include <gurobi_c++.h>

class CoffeeDistributionOptimizer {
public:
    explicit CoffeeDistributionOptimizer(const DistributionNetwork& network) : network(network) {}

    void create_variables();
    void set_objective();
    void add_constraints();
    void add_customized_constraint(const GRBConstr& constraint);
    void optimize();
    void run();
    void log_solution(const std::string& output_file, const std::string& header = "");

private:
    DistributionNetwork network;
    GRBEnv env;
    GRBModel model;
    std::vector<GRBVar> variables;
};