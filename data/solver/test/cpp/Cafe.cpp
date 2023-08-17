#include "Cafe.h"
#include <iostream>

void Cafe::display_info() const {
    std::cout << "Name: " << name << "\nLocation: " << location << "\nContact: " << contact << "\nCoffee Demand:\n";
    for (const auto& demand : coffee_demand) {
        std::cout << "  - " << demand.first << ": " << demand.second << "\n";
    }
}

std::string Cafe::to_string() const {
    return "Cafe(name=" + name + ", location=" + location + ", contact=" + contact + ")";
}