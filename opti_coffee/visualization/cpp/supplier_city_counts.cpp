#include "csv.h"
#include <iostream>
#include <unordered_map>
#include <string>
#include <utility>
#include <fstream>
#include <cstdlib>

// ... (same as before)

int main() {
    auto city_counts = get_city_counts();
    write_city_counts_to_file(city_counts);

    // Call the Python script to create the map
    std::system("python plot_supplier_map.py");

    return 0;
}