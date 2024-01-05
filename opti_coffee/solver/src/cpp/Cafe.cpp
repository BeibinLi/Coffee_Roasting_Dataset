#include "Cafe.h"
#include <iostream>
#include <stdexcept>

void Cafe::display_info() const {
    std::cout << "Name: " << name << "\nLocation: " << location << "\nContact: " << contact << "\nCoffee Demand:\n";
    for (const auto& demand : coffee_demand) {
        std::cout << "  - " << demand.first << ": " << demand.second << "\n";
    }
}

std::string Cafe::to_string() const {
    return "Cafe(name=" + name + ", location=" + location + ", contact=" + contact + ")";
}

void Cafe::fulfill_demand(const std::string& coffee_type, int quantity) {
    int current_demand = get_coffee_demand(coffee_type);
    if (quantity > current_demand) {
        throw std::runtime_error("Fulfilled quantity exceeds demand");
    }
    coffee_demand[coffee_type] = current_demand - quantity;
}