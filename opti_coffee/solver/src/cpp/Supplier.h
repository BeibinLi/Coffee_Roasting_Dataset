#pragma once
#include <string>
#include <unordered_map>

class Supplier {
public:
    Supplier(const std::string& name, int capacity, const std::string& location, const std::string& contact)
        : name(name), capacity(capacity), location(location), contact(contact) {}

    void set_shipping_cost(const std::string& roastery_name, double cost) {
        shipping_costs[roastery_name] = cost;
    }

    double get_shipping_cost(const std::string& roastery_name) const {
        auto it = shipping_costs.find(roastery_name);
        return it != shipping_costs.end() ? it->second : std::numeric_limits<double>::infinity();
    }

    bool validate_capacity(int requested_quantity) const {
        return requested_quantity <= capacity;
    }

    void reduce_capacity(int quantity);
    void increase_capacity(int quantity);

    void display_info() const;
    std::string to_string() const;

    const std::unordered_map<std::string, double>& get_shipping_costs() const {
        return shipping_costs;
    }

    const std::string& get_name() const {
        return name;
    }

    int get_capacity() const {
        return capacity;
    }

    const std::string& get_location() const {
        return location;
    }

    const std::string& get_contact() const {
        return contact;
    }

private:
    std::string name;
    int capacity;
    std::string location;
    std::string contact;
    std::unordered_map<std::string, double> shipping_costs;
};