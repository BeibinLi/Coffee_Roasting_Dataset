#include "matplotlibcpp.h"
#include "csv.h"
#include <vector>
#include <string>
#include <map>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <filesystem>

namespace plt = matplotlibcpp;

std::map<std::string, int> get_data() {
    std::map<std::string, int> membership_counts;
    io::CSVReader<1> in("database/customer.csv");
    in.read_header(io::ignore_extra_column, "member_since");
    std::string member_since;
    while (in.read_row(member_since)) {
        std::tm tm = {};
        std::istringstream ss(member_since);
        ss >> std::get_time(&tm, "%Y-%m-%d");
        std::ostringstream year_month;
        year_month << std::put_time(&tm, "%Y-%m");
        membership_counts[year_month.str()]++;
    }
    return membership_counts;
}

void plot(const std::map<std::string, int>& membership_counts) {
    std::vector<std::string> x;
    std::vector<int> y;
    for (const auto& entry : membership_counts) {
        x.push_back(entry.first);
        y.push_back(entry.second);
    }

    plt::figure_size(1200, 500);
    plt::bar(x, y, 0.5, "skyblue");
    plt::title("Duration of Membership (Monthly)");
    plt::xlabel("Year-Month");
    plt::ylabel("Number of Customers Joined");
    plt::xticks_rotation(45);
    plt::tight_layout();

    std::filesystem::create_directories("images");
    plt::save("images/membership_duration.png");
}

int main() {
    auto membership_counts = get_data();
    plot(membership_counts);

    return 0;
}