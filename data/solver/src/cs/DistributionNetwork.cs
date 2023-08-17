using System;
using System.Collections.Generic;

namespace CoffeeDistribution.Entities
{
    public class DistributionNetwork
    {
        public List<Supplier> Suppliers { get; private set; }
        public List<Roastery> Roasteries { get; private set; }
        public List<Cafe> Cafes { get; private set; }
        public Dictionary<(string, string), double> ShippingCostFromSupplierToRoastery { get; private set; }
        public Dictionary<(string, string), double> ShippingCostFromRoasteryToCafe { get; private set; }

        public DistributionNetwork()
        {
            Suppliers = new List<Supplier>();
            Roasteries = new List<Roastery>();
            Cafes = new List<Cafe>();
            ShippingCostFromSupplierToRoastery = new Dictionary<(string, string), double>();
            ShippingCostFromRoasteryToCafe = new Dictionary<(string, string), double>();
        }

        public void AddSupplier(Supplier supplier)
        {
            Suppliers.Add(supplier);
        }

        public void AddRoastery(Roastery roastery)
        {
            Roasteries.Add(roastery);
        }

        public void AddCafe(Cafe cafe)
        {
            Cafes.Add(cafe);
        }

        public void SetShippingCostFromSupplierToRoastery(Supplier supplier, Roastery roastery, double cost)
        {
            ShippingCostFromSupplierToRoastery[(supplier.Name, roastery.Name)] = cost;
        }

        public void SetShippingCostFromRoasteryToCafe(Roastery roastery, Cafe cafe, double cost)
        {
            ShippingCostFromRoasteryToCafe[(roastery.Name, cafe.Name)] = cost;
        }

        public double GetShippingCostFromSupplierToRoastery(string supplierName, string roasteryName)
        {
            return ShippingCostFromSupplierToRoastery.TryGetValue((supplierName, roasteryName), out double cost) ? cost : double.PositiveInfinity;
        }

        public double GetShippingCostFromRoasteryToCafe(string roasteryName, string cafeName)
        {
            return ShippingCostFromRoasteryToCafe.TryGetValue((roasteryName, cafeName), out double cost) ? cost : double.PositiveInfinity;
        }

        public void DisplayNetworkInfo()
        {
            Console.WriteLine("Suppliers:");
            foreach (var supplier in Suppliers)
            {
                Console.WriteLine(supplier);
            }

            Console.WriteLine("\nRoasteries:");
            foreach (var roastery in Roasteries)
            {
                Console.WriteLine(roastery);
            }

            Console.WriteLine("\nCafes:");
            foreach (var cafe in Cafes)
            {
                Console.WriteLine(cafe);
            }
        }
    }
}