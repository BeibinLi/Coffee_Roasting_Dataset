#pragma once
#include <string>
#include <unordered_map>

class Cafe {
public:
    Cafe(const std::string& name, const std::string& location, const std::string& contact)
        : name(name), location(location), contact(contact) {}

    void set_coffee_demand(const std::string& product_id, int quantity) {
        coffee_demand[product_id] = quantity;
    }

private:
    std::string name;
    std::string location;
    std::string contact;
    std::unordered_map<std::string, int> coffee_demand;
};