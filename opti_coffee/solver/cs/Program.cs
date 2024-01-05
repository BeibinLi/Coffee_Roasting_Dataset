using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using CsvHelper;
using CoffeeDistribution.Entities;
using CoffeeDistribution.Optimizer;

namespace CoffeeDistribution
{
    class Program
    {
        static void Main(string[] args)
        {
            int year = 2023;
            int month = 12;
            string baseDir = "../database/";

            // Read Suppliers from CSV
            var supplierMap = new Dictionary<int, Supplier>();
            using (var reader = new StreamReader(baseDir + "supplier.csv"))
            using (var csv = new CsvReader(reader, System.Globalization.CultureInfo.InvariantCulture))
            {
                var records = csv.GetRecords<SupplierRecord>();
                foreach (var record in records)
                {
                    var supplier = new Supplier(record.ContactName, record.MaxPurchaseThisYear, record.City, record.PhoneNumber);
                    supplierMap[record.SupplierId] = supplier;
                }
            }

            // Read Demand (Cafes) from CSV
            var demandHistory = new List<DemandHistoryRecord>();
            using (var reader = new StreamReader(baseDir + "demand_history.csv"))
            using (var csv = new CsvReader(reader, System.Globalization.CultureInfo.InvariantCulture))
            {
                demandHistory = csv.GetRecords<DemandHistoryRecord>().ToList();
            }

            var productIds = demandHistory.Select(x => x.ProductId).Distinct().ToList();
            var demand = demandHistory.Where(x => x.Year == year && x.Month == month).ToList();

            var cafeMap = new Dictionary<int, Cafe>();
            using (var reader = new StreamReader(baseDir + "customer.csv"))
            using (var csv = new CsvReader(reader, System.Globalization.CultureInfo.InvariantCulture))
            {
                var records = csv.GetRecords<CustomerRecord>();
                foreach (var record in records)
                {
                    var cafe = new Cafe(record.CafeName, record.City + ", " + record.Country, record.ContactName);
                    cafeMap[record.CustomerId] = cafe;
                }
            }

            double income = 0;
            var sellPriceHistory = new List<SellPriceHistoryRecord>();
            using (var reader = new StreamReader(baseDir + "sell_price_history.csv"))
            using (var csv = new CsvReader(reader, System.Globalization.CultureInfo.InvariantCulture))
            {
                sellPriceHistory = csv.GetRecords<SellPriceHistoryRecord>().ToList();
            }

            var sellPrice = sellPriceHistory.Where(x => x.Year == year && x.Month == month).ToList();
            foreach (var record in demand)
            {
                var cafe = cafeMap[record.CustomerId];
                cafe.SetCoffeeDemand(record.ProductId.ToString(), record.Quantity);
                income += sellPrice.First(x => x.RoastingId == record.ProductId).PricePerUnit * record.Quantity;
            }

            Console.WriteLine($"Total income: {income}");

            // Read Roasteries from CSV
            var roasteryMap = new Dictionary<int, Roastery>();
            using (var reader = new StreamReader(baseDir + $"roastery_{year}.csv"))
            using (var csv = new CsvReader(reader, System.Globalization.CultureInfo.InvariantCulture))
            {
                var records = csv.GetRecords<RoasteryRecord>();
                foreach (var record in records)
                {
                    var roastery = new Roastery($"Roastery {record.RoasteryId}", record.ContactEmail, record.City);
                    foreach (var productId in productIds)
                    {
                        roastery.SetRoastingCost(productId.ToString(), record.RoastCost[productId]);
                    }
                    roasteryMap[record.RoasteryId] = roastery;
                }
            }

            // Creating the DistributionNetwork instance using the shipping costs
            var network = new DistributionNetwork();

            // Add suppliers, roasteries, and cafes to the network
            foreach (var supplier in supplierMap.Values) network.AddSupplier(supplier);
            foreach (var roastery in roasteryMap.Values) network.AddRoastery(roastery);
            foreach (var cafe in cafeMap.Values) network.AddCafe(cafe);

            // Set shipping costs for suppliers to roasteries
            var supplyPriceHistory = new List<SupplyPriceHistoryRecord>();
            using (var reader = new StreamReader(baseDir + "supply_price_history.csv"))
            using (var csv = new CsvReader(reader, System.Globalization.CultureInfo.InvariantCulture))
            {
                supplyPriceHistory = csv.GetRecords<SupplyPriceHistoryRecord>().ToList();
            }

            var supplyPrice = supplyPriceHistory.Where(x => x.Year == year && x.Month == month).ToList();
            foreach (var roastery in roasteryMap)
            {
                foreach (var supplier in supplierMap)
                {
                    double cost = roastery.Value.ShipCostSupply[supplier.Key] + supplyPrice.First(x => x.SupplierId == supplier.Key).PricePerUnit;
                    network.SetShippingCostFromSupplierToRoastery(supplier.Value, roastery.Value, cost);
                }
            }

            // Set shipping costs for roasteries to cafes
            foreach (var roastery in roasteryMap)
            {
                foreach (var cafe in cafeMap)
                {
                    double cost = roastery.Value.ShipCostCustomer[cafe.Key];
                    network.SetShippingCostFromRoasteryToCafe(roastery.Value, cafe.Value, cost);
                }
            }

            // Create and run the optimizer
            var optimizer = new CoffeeDistributionOptimizer(network);
            optimizer.Run();

            double totalCost = optimizer.Model.ObjVal;

            double totalSalary = 0;
            using (var reader = new StreamReader(baseDir + "employee.csv"))
            using (var csv = new CsvReader(reader, System.Globalization.CultureInfo.InvariantCulture))
            {
                totalSalary = csv.GetRecords<EmployeeRecord>().Sum(x => x.Salary) / 12.0;
            }

            double profit = income - totalCost - totalSalary;

            string summary = $@"
--------------------------
Total Revenue: {income:.2f}
Purchasing and Shipping Cost: {totalCost:.2f}
Salary: {totalSalary:.2f}
Total Profit: {profit:.2f}
--------------------------
";
            Console.WriteLine(summary);

            optimizer.LogSolution($"output/solution_{year}_{month}.md", summary);

            Console.WriteLine("=".PadRight(60, '='));
            Console.WriteLine("\n\n");
        }
    }
}