#include "matplotlibcpp.h"
#include "csv.h"
#include <vector>
#include <string>
#include <algorithm>
#include <filesystem>

namespace plt = matplotlibcpp;

void plot(const std::vector<int>& salaries, int salary_quantum) {
    int min_salary = *std::min_element(salaries.begin(), salaries.end()) / salary_quantum * salary_quantum;
    int max_salary = (*std::max_element(salaries.begin(), salaries.end()) + salary_quantum - 1) / salary_quantum * salary_quantum;
    std::vector<int> bins;
    for (int i = min_salary; i <= max_salary; i += salary_quantum) {
        bins.push_back(i);
    }

    plt::hist(salaries, bins, "skyblue", "black", 0.7);
    plt::title("Distribution of Salaries");
    plt::xlabel("Salary Amount");
    plt::ylabel("Frequency");
    plt::grid(true, "both", "y");

    plt::tight_layout();
    std::filesystem::create_directories("images");
    plt::save("images/salary.png");
}

int main() {
    std::vector<int> salaries;
    io::CSVReader<1> in("database/employee.csv");
    in.read_header(io::ignore_extra_column, "salary");
    int salary;
    while (in.read_row(salary)) {
        salaries.push_back(salary);
    }

    plot(salaries, 1000);

    return 0;
}