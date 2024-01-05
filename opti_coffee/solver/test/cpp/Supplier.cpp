#include "Supplier.h"

std::string Supplier::to_string() const {
    return "Supplier(name=" + name + ", capacity=" + std::to_string(capacity) + ", location=" + location + ", contact=" + contact + ")";
}

bool Supplier::validate_capacity(int requested_capacity) const {
    return requested_capacity <= capacity;
}