#pragma once
#include "DistributionNetwork.h"

class CoffeeDistributionOptimizer {
public:
    explicit CoffeeDistributionOptimizer(const DistributionNetwork& network) : network(network) {}

    void run();
    double get_total_cost() const;
    void log_solution(const std::string& filename) const;

private:
    DistributionNetwork network;
    double total_cost;
};