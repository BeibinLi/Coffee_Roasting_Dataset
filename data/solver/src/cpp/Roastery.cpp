#include "Roastery.h"
#include <iostream>

bool Roastery::validate_roasting_constraints(const std::string& coffee_type, const std::string& constraints) const {
    const std::string& required_constraints = get_roasting_constraints(coffee_type);
    return required_constraints.empty() || required_constraints == constraints;
}

void Roastery::display_info() const {
    std::cout << "Name: " << name << "\nLocation: " << location << "\nContact: " << contact << "\nRoasting Costs:\n";
    for (const auto& cost : roasting_costs) {
        std::cout << "  - " << cost.first << ": " << cost.second.cost << " (Constraints: " << cost.second.constraints << ")\n";
    }
    std::cout << "Shipping Costs:\n";
    for (const auto& cost : shipping_costs) {
        std::cout << "  - " << cost.first << ": " << cost.second << "\n";
    }
}

std::string Roastery::to_string() const {
    return "Roastery(name=" + name + ", location=" + location + ", contact=" + contact + ")";
}