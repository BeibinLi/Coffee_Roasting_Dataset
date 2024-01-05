#include "matplotlibcpp.h"
#include "csv.h"
#include <vector>
#include <string>
#include <map>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <filesystem>
#include <iostream>

namespace plt = matplotlibcpp;

int get_supplier_id(int supplier_id, const std::string& supplier_name) {
    if (supplier_id == 0 && supplier_name.empty()) {
        throw std::runtime_error("Either --id or --name must be specified.");
    }

    if (supplier_id == 0) {
        io::CSVReader<5> in("database/supplier.csv");
        in.read_header(io::ignore_extra_column, "supplier_id", "contact_name", "max_purchase_this_year", "city", "phone_number");
        int id;
        std::string name, city, phone_number;
        int max_purchase_this_year;
        while (in.read_row(id, name, max_purchase_this_year, city, phone_number)) {
            if (name == supplier_name) {
                supplier_id = id;
                break;
            }
        }
        if (supplier_id == 0) {
            throw std::runtime_error("No supplier with name " + supplier_name + " found.");
        }
    }

    return supplier_id;
}

std::map<std::string, double> get_data(int supplier_id) {
    std::map<std::string, double> data;
    io::CSVReader<4> in("database/supply_price_history.csv");
    in.read_header(io::ignore_extra_column, "year", "month", "supplier_id", "price_per_unit");
    int year, month, id;
    double price_per_unit;
    while (in.read_row(year, month, id, price_per_unit)) {
        if (id == supplier_id) {
            std::ostringstream date;
            date << year << "-" << std::setfill('0') << std::setw(2) << month << "-01";
            data[date.str()] = price_per_unit;
        }
    }
    return data;
}

void plot(const std::map<std::string, double>& data, int supplier_id) {
    std::vector<std::string> x;
    std::vector<double> y;
    for (const auto& entry : data) {
        x.push_back(entry.first);
        y.push_back(entry.second);
    }

    plt::plot(x, y, "b-o");
    plt::title("Change in Supply Price for Supplier " + std::to_string(supplier_id));
    plt::xlabel("Date");
    plt::ylabel("Price per Unit");
    plt::grid(true);
    plt::tight_layout();

    std::filesystem::create_directories("images");
    plt::save("images/supplier_price_" + std::to_string(supplier_id) + ".png");
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " --id <supplier_id> or " << argv[0] << " --name <supplier_name>" << std::endl;
        return 1;
    }

    int supplier_id = 0;
    std::string supplier_name;
    if (std::string(argv[1]) == "--id") {
        supplier_id = std::stoi(argv[2]);
    } else if (std::string(argv[1]) == "--name") {
        supplier_name = argv[2];
    } else {
        std::cerr << "Invalid option: " << argv[1] << std::endl;
        return 1;
    }

    supplier_id = get_supplier_id(supplier_id, supplier_name);
    auto data = get_data(supplier_id);
    plot(data, supplier_id);

    return 0;
}