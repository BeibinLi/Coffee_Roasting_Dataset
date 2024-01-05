#pragma once
#include <string>
#include <unordered_map>

class Roastery {
public:
    Roastery(const std::string& name, const std::string& contact, const std::string& location)
        : name(name), contact(contact), location(location) {}

    void set_roasting_cost(const std::string& product_id, double cost) {
        roasting_costs[product_id] = cost;
    }

private:
    std::string name;
    std::string contact;
    std::string location;
    std::unordered_map<std::string, double> roasting_costs;
};