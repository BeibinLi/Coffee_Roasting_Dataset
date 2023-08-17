#pragma once
#include "Supplier.h"
#include "Roastery.h"
#include "Cafe.h"
#include <vector>

class DistributionNetwork {
public:
    void add_supplier(const Supplier& supplier);
    void add_roastery(const Roastery& roastery);
    void add_cafe(const Cafe& cafe);

    void set_shipping_cost_from_supplier_to_roastery(const Supplier& supplier, const Roastery& roastery, double cost);
    void set_shipping_cost_from_roastery_to_cafe(const Roastery& roastery, const Cafe& cafe, double cost);

private:
    std::vector<Supplier> suppliers;
    std::vector<Roastery> roasteries;
    std::vector<Cafe> cafes;
};