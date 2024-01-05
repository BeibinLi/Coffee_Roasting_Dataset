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

    int get_coffee_demand(const std::string& product_id) const {
        auto it = coffee_demand.find(product_id);
        return it != coffee_demand.end() ? it->second : 0;
    }

    const std::unordered_map<std::string, int>& get_coffee_demand() const {
        return coffee_demand;
    }

    const std::string& get_name() const {
        return name;
    }

    const std::string& get_location() const {
        return location;
    }

    const std::string& get_contact() const {
        return contact;
    }

    void display_info() const;
    std::string to_string() const;

private:
    std::string name;
    std::string location;
    std::string contact;
    std::unordered_map<std::string, int> coffee_demand;
};