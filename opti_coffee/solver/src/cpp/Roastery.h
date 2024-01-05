#pragma once
#include <string>
#include <unordered_map>

struct RoastingCost {
    double cost;
    std::string constraints;
};

class Roastery {
public:
    Roastery(const std::string& name, const std::string& contact, const std::string& location)
        : name(name), contact(contact), location(location) {}

    void set_roasting_cost(const std::string& coffee_type, double cost, const std::string& constraints) {
        roasting_costs[coffee_type] = {cost, constraints};
    }

    void set_shipping_cost(const std::string& cafe_name, double cost) {
        shipping_costs[cafe_name] = cost;
    }

    double get_shipping_cost(const std::string& cafe_name) const {
        auto it = shipping_costs.find(cafe_name);
        return it != shipping_costs.end() ? it->second : std::numeric_limits<double>::infinity();
    }

    double get_roasting_cost(const std::string& coffee_type) const {
        auto it = roasting_costs.find(coffee_type);
        return it != roasting_costs.end() ? it->second.cost : std::numeric_limits<double>::infinity();
    }

    const std::string& get_roasting_constraints(const std::string& coffee_type) const {
        auto it = roasting_costs.find(coffee_type);
        return it != roasting_costs.end() ? it->second.constraints : "";
    }

    bool validate_roasting_constraints(const std::string& coffee_type, const std::string& constraints) const;

    void display_info() const;
    std::string to_string() const;

    const std::unordered_map<std::string, RoastingCost>& get_roasting_costs() const {
        return roasting_costs;
    }

    const std::unordered_map<std::string, double>& get_shipping_costs() const {
        return shipping_costs;
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

private:
    std::string name;
    std::string contact;
    std::string location;
    std::unordered_map<std::string, RoastingCost> roasting_costs;
    std::unordered_map<std::string, double> shipping_costs;
};