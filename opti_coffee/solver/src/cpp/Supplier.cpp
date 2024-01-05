#include "Supplier.h"
#include <iostream>
#include <stdexcept>

void Supplier::reduce_capacity(int quantity) {
    if (validate_capacity(quantity)) {
        capacity -= quantity;
    } else {
        throw std::runtime_error("Requested quantity exceeds capacity");
    }
}

void Supplier::increase_capacity(int quantity) {
    capacity += quantity;
}

void Supplier::display_info() const {
    std::cout << "Name: " << name << "\nCapacity: " << capacity << "\nLocation: " << location << "\nContact: " << contact << "\nShipping Costs:\n";
    for (const auto& cost : shipping_costs) {
        std::cout << "  - " << cost.first << ": " << cost.second << "\n";
    }
}

std::string Supplier::to_string() const {
    return "Supplier(name=" + name + ", capacity=" + std::to_string(capacity) + ", location=" + location + ", contact=" + contact + ")";
}