#pragma once
#include "Supplier.h"
#include "Roastery.h"
#include "Cafe.h"
#include <vector>
#include <map>
#include <utility>

class DistributionNetwork {
public:
    void add_supplier(const Supplier& supplier);
    void add_roastery(const Roastery& roastery);
    void add_cafe(const Cafe& cafe);

    void set_shipping_cost_from_supplier_to_roastery(const Supplier& supplier, const Roastery& roastery, double cost);
    void set_shipping_cost_from_roastery_to_cafe(const Roastery& roastery, const Cafe& cafe, double cost);

    double get_shipping_cost_from_supplier_to_roastery(const std::string& supplier_name, const std::string& roastery_name) const;
    double get_shipping_cost_from_roastery_to_cafe(const std::string& roastery_name, const std::string& cafe_name) const;

    void display_network_info() const;

private:
    std::vector<Supplier> suppliers;
    std::vector<Roastery> roasteries;
    std::vector<Cafe> cafes;
    std::map<std::pair<std::string, std::string>, double> shipping_cost_from_supplier_to_roastery;
    std::map<std::pair<std::string, std::string>, double> shipping_cost_from_roastery_to_cafe;
};