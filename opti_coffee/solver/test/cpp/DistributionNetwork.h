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

    const std::vector<Supplier>& get_suppliers() const;
    const std::vector<Roastery>& get_roasteries() const;
    const std::vector<Cafe>& get_cafes() const;

    double get_shipping_cost_from_supplier_to_roastery(const Supplier& supplier, const Roastery& roastery) const;
    double get_shipping_cost_from_roastery_to_cafe(const Roastery& roastery, const Cafe& cafe) const;

private:
    std::vector<Supplier> suppliers;
    std::vector<Roastery> roasteries;
    std::vector<Cafe> cafes;
    std::map<std::pair<std::string, std::string>, double> shipping_cost_from_supplier_to_roastery;
    std::map<std::pair<std::string, std::string>, double> shipping_cost_from_roastery_to_cafe;
};