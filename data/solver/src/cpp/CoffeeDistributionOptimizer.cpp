#include "CoffeeDistributionOptimizer.h"
#include <iostream>
#include <fstream>
#include <stdexcept>

void CoffeeDistributionOptimizer::create_variables() {
    // Create optimization variables for shipping and roasting
    // ...
}

void CoffeeDistributionOptimizer::set_objective() {
    // Set the objective function to minimize the total cost
    // ...
}

void CoffeeDistributionOptimizer::add_constraints() {
    // Add constraints for flow conservation, supply, demand, and specific roasting constraints
    // ...
}

void CoffeeDistributionOptimizer::add_customized_constraint(const GRBConstr& constraint) {
    model.addConstr(constraint);
}

void CoffeeDistributionOptimizer::optimize() {
    model.optimize();
    if (model.get(GRB_IntAttr_Status) == GRB_OPTIMAL) {
        std::cout << "Optimal cost: " << model.get(GRB_DoubleAttr_ObjVal) << std::endl;
    } else {
        std::cout << "Not solved to optimality. Optimization status: " << model.get(GRB_IntAttr_Status) << std::endl;
    }
}

void CoffeeDistributionOptimizer::run() {
    create_variables();
    set_objective();
    add_constraints();
    optimize();
}

void CoffeeDistributionOptimizer::log_solution(const std::string& output_file, const std::string& header) {
    std::ofstream file(output_file);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open output file");
    }

    file << header << "\n";
    if (model.get(GRB_IntAttr_Status) != GRB_OPTIMAL) {
        file << "No optimal solution found. Cannot log the solution.";
        return;
    }

    file << "\nOptimal Solution:\n";
    for (const auto& var : model.getVars()) {
        if (var.get(GRB_DoubleAttr_X) != 0) {  // Only print non-zero variables
            file << var.get(GRB_StringAttr_VarName) << ": " << var.get(GRB_DoubleAttr_X) << "\n";
        }
    }
    file.close();
}