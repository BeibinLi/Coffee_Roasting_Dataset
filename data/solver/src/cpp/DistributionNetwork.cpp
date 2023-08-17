#include "DistributionNetwork.h"
#include <iostream>

void DistributionNetwork::add_supplier(const Supplier& supplier) {
    suppliers.push_back(supplier);
}

void DistributionNetwork::add_roastery(const Roastery& roastery) {
    roasteries.push_back(roastery);
}

void DistributionNetwork::add_cafe(const Cafe& cafe) {
    cafes.push_back(cafe);
}

void DistributionNetwork::set_shipping_cost_from_supplier_to_roastery(const Supplier& supplier, const Roastery& roastery, double cost) {
    shipping_cost_from_supplier_to_roastery[std::make_pair(supplier.get_name(), roastery.get_name())] = cost;
}

void DistributionNetwork::set_shipping_cost_from_roastery_to_cafe(const Roastery& roastery, const Cafe& cafe, double cost) {
    shipping_cost_from_roastery_to_cafe[std::make_pair(roastery.get_name(), cafe.get_name())] = cost;
}

double DistributionNetwork::get_shipping_cost_from_supplier_to_roastery(const std::string& supplier_name, const std::string& roastery_name) const {
    auto it = shipping_cost_from_supplier_to_roastery.find(std::make_pair(supplier_name, roastery_name));
    return it != shipping_cost_from_supplier_to_roastery.end() ? it->second : std::numeric_limits<double>::infinity();
}

double DistributionNetwork::get_shipping_cost_from_roastery_to_cafe(const std::string& roastery_name, const std::string& cafe_name) const {
    auto it = shipping_cost_from_roastery_to_cafe.find(std::make_pair(roastery_name, cafe_name));
    return it != shipping_cost_from_roastery_to_cafe.end() ? it->second : std::numeric_limits<double>::infinity();
}

void DistributionNetwork::display_network_info() const {
    std::cout << "Suppliers:" << std::endl;
    for (const auto& supplier : suppliers) {
        std::cout << supplier.to_string() << std::endl;
    }
    std::cout << "\nRoasteries:" << std::endl;
    for (const auto& roastery : roasteries) {
        std::cout << roastery.to_string() << std::endl;
    }
    std::cout << "\nCafes:" << std::endl;
    for (const auto& cafe : cafes) {
        std::cout << cafe.to_string() << std::endl;
    }
}