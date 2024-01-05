#include "matplotlibcpp.h"
#include "csv.h"
#include <vector>
#include <string>
#include <map>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <filesystem>
#include <algorithm>
#include <iostream>

namespace plt = matplotlibcpp;

std::map<std::string, std::vector<double>> get_data(const std::string& bean_name) {
    std::map<std::string, std::vector<double>> data;
    io::CSVReader<4> in("database/sell_price_history.csv");
    in.read_header(io::ignore_extra_column, "year", "month", "source_bean_type", "price_per_unit");
    int year, month;
    std::string source_bean_type;
    double price_per_unit;
    while (in.read_row(year, month, source_bean_type, price_per_unit)) {
        if (source_bean_type == bean_name) {
            std::ostringstream date;
            date << year << "-" << std::setfill('0') << std::setw(2) << month << "-01";
            data[date.str()].push_back(price_per_unit);
        }
    }
    return data;
}

void plot_data(const std::map<std::string, std::vector<double>>& data, const std::string& bean_name) {
    std::vector<std::string> x;
    std::vector<double> y_min, y_max, y_mean;
    for (const auto& entry : data) {
        x.push_back(entry.first);
        auto minmax = std::minmax_element(entry.second.begin(), entry.second.end());
        y_min.push_back(*minmax.first);
        y_max.push_back(*minmax.second);
        y_mean.push_back(std::accumulate(entry.second.begin(), entry.second.end(), 0.0) / entry.second.size());
    }

    plt::figure_size(1200, 600);
    plt::fill_between(x, y_min, y_max, "skyblue", 0.4, "Price Range (Min to Max)");
    plt::plot(x, y_mean, "blue", "o", "Mean Price");
    plt::title("Bean Price Chart for " + bean_name);
    plt::xlabel("Time");
    plt::ylabel("Price");
    plt::legend();
    plt::tight_layout();
    plt::grid(true, "both", "both", "--", 0.5);

    std::filesystem::create_directories("images");
    plt::save("images/bean_price_" + bean_name + ".png");
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <bean_name>" << std::endl;
        return 1;
    }

    std::string bean_name = argv[1];
    std::transform(bean_name.begin(), bean_name.end(), bean_name.begin(), ::tolower);

    auto data = get_data(bean_name);
    plot_data(data, bean_name);

    return 0;
}