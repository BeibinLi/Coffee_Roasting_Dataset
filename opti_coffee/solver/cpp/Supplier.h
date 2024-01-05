#pragma once
#include <string>

class Supplier {
public:
    Supplier(const std::string& name, int capacity, const std::string& location, const std::string& contact)
        : name(name), capacity(capacity), location(location), contact(contact) {}

private:
    std::string name;
    int capacity;
    std::string location;
    std::string contact;
};