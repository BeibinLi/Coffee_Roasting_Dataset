#pragma once
#include <string>
#include <unordered_map>

class Cafe {
public:
    Cafe(const std::string& name, const std::string& location, const std::string& contact)
        : name(name), location(location), contact(contact) {}

    void set_coffee_demand(const std::string& coffee_type, int quantity) {
        coffee_demand[coffee_type] = quantity;
    }

    int get_coffee_demand(const std::string& coffee_type) const {
        auto it = coffee_demand.find(coffee_type);
        return it != coffee_demand.end() ? it->second : 0;
    }

    void display_info() const;
    std::string to_string() const;
    void fulfill_demand(const std::string& coffee_type, int quantity);

private:
    std::string name;
    std::string location;
    std::string contact;
    std::unordered_map<std::string, int> coffee_demand;
};