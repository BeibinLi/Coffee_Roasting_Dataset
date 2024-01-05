#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <iomanip>
#include "Supplier.h"
#include "Roastery.h"
#include "Cafe.h"
#include "DistributionNetwork.h"
#include "CoffeeDistributionOptimizer.h"

int main(int argc, char* argv[]) {
    int year = 2023;
    int month = 12;
    std::string base_dir = "../database/";

    // Parse command line arguments
    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        if (arg == "--year" || arg == "-y") {
            year = std::stoi(argv[++i]);
        } else if (arg == "--month" || arg == "-m") {
            month = std::stoi(argv[++i]);
        } else if (arg == "--base_dir" || arg == "-b") {
            base_dir = argv[++i];
        }
    }

    // Read Suppliers from CSV
    std::unordered_map<int, Supplier> supplier_map;
    std::ifstream supplier_file(base_dir + "supplier.csv");
    std::string line;
    std::getline(supplier_file, line); // Skip header
    while (std::getline(supplier_file, line)) {
        std::istringstream ss(line);
        std::vector<std::string> tokens;
        std::string token;
        while (std::getline(ss, token, ',')) {
            tokens.push_back(token);
        }
        int sid = std::stoi(tokens[0]);
        supplier_map[sid] = Supplier(tokens[1], std::stoi(tokens[2]), tokens[3], tokens[4]);
    }
    supplier_file.close();

    // Read Demand (Cafes) from CSV
    // ... (similar to reading suppliers)

    // Calculate total income
    double income = 0;
    // ... (calculate income based on demand and sell_price)

    std::cout << "Total income: " << income << std::endl;

    // Read Roasteries from CSV
    std::unordered_map<int, Roastery> roastery_map;
    // ... (similar to reading suppliers)

    // Create Distribution Network
    DistributionNetwork network;
    for (const auto& s : supplier_map) {
        network.add_supplier(s.second);
    }
    for (const auto& r : roastery_map) {
        network.add_roastery(r.second);
    }
    for (const auto& c : cafe_map) {
        network.add_cafe(c.second);
    }

    // Set shipping costs for suppliers to roasteries
    // ... (similar to reading suppliers and setting costs)

    // Set shipping costs for roasteries to cafes
    // ... (similar to reading suppliers and setting costs)

    // Create and run the optimizer
    CoffeeDistributionOptimizer optimizer(network);
    optimizer.run();

    double total_cost = optimizer.get_total_cost();

    // Read employee salaries and calculate total salary
    double total_salary = 0;
    // ... (similar to reading suppliers and calculating total_salary)

    double profit = income - total_cost - total_salary;

    std::cout << std::fixed << std::setprecision(2)
              << "--------------------------\n"
              << "Total Revenue: " << income << "\n"
              << "Purchasing and Shipping Cost: " << total_cost << "\n"
              << "Salary: " << total_salary << "\n"
              << "Total Profit: " << profit << "\n"
              << "--------------------------\n";

    optimizer.log_solution("output/solution_" + std::to_string(year) + "_" + std::to_string(month) + ".md");

    std::cout << std::string(60, '=') << std::endl << std::endl;

    return 0;
}