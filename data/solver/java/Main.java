import java.io.*;
import java.util.*;
import java.nio.file.*;
import java.util.stream.Collectors;
import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;

public class Main {
    public static void main(String[] args) {
        // Read arguments
        int year = 2023;
        int month = 12;
        String baseDir = "../database/";

        for (int i = 0; i < args.length; i++) {
            if (args[i].equals("--year") || args[i].equals("-y")) {
                year = Integer.parseInt(args[++i]);
            } else if (args[i].equals("--month") || args[i].equals("-m")) {
                month = Integer.parseInt(args[++i]);
            } else if (args[i].equals("--base_dir") || args[i].equals("-b")) {
                baseDir = args[++i];
            }
        }

        // Read Suppliers from CSV
        Map<String, Supplier> supplierMap = readSuppliersFromCSV(baseDir + "supplier.csv");

        // Read Demand (Cafes) from CSV
        List<String> productIds = readProductIdsFromCSV(baseDir + "demand_history.csv", year, month);
        Map<String, Cafe> cafeMap = readCafesFromCSV(baseDir, year, month, productIds);

        // Calculate total income
        double income = calculateTotalIncome(baseDir, year, month, cafeMap);

        System.out.printf("Total income: %.2f%n", income);

        // Read Roasteries from CSV
        Map<String, Roastery> roasteryMap = readRoasteriesFromCSV(baseDir + "roastery_" + year + ".csv", productIds);

        // Creating the DistributionNetwork instance using the shipping costs
        DistributionNetwork network = new DistributionNetwork();

        // Create Distribution Network
        network.addSuppliers(supplierMap.values());
        network.addRoasteries(roasteryMap.values());
        network.addCafes(cafeMap.values());

        // Set shipping costs for suppliers to roasteries
        setShippingCostsFromSuppliersToRoasteries(baseDir, year, month, supplierMap, roasteryMap, network);

        // Set shipping costs for roasteries to cafes
        setShippingCostsFromRoasteriesToCafes(roasteryMap, cafeMap, network);

        // Create and run the optimizer
        CoffeeDistributionOptimizer optimizer = new CoffeeDistributionOptimizer(network);
        optimizer.run();

        double totalCost = optimizer.getModel().getObjVal();

        // Calculate total salary
        double totalSalary = calculateTotalSalary(baseDir);

        double profit = income - totalCost - totalSalary;

        String summary = String.format(
                """
                --------------------------
                Total Revenue: %.2f
                Purchasing and Shipping Cost: %.2f
                Salary: %.2f
                Total Profit: %.2f
                --------------------------
                """,
                income, totalCost, totalSalary, profit
        );
        System.out.println(summary);

        optimizer.logSolution("output/solution_" + year + "_" + month + ".md", summary);

        System.out.println("=".repeat(60));
        System.out.println("\n\n");
    }

    // Helper methods for reading data from CSV files and setting shipping costs
}