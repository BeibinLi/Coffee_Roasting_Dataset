using Xunit;
using CoffeeDistribution.Entities;

namespace CoffeeDistribution.Tests
{
    public class DistributionNetworkTests
    {
        [Fact]
        public void TestAddSupplier()
        {
            var network = new DistributionNetwork();
            var supplier = new Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
            network.AddSupplier(supplier);
            Assert.Single(network.Suppliers);
            Assert.Equal(supplier, network.Suppliers[0]);
        }

        [Fact]
        public void TestAddRoastery()
        {
            var network = new DistributionNetwork();
            var roastery = new Roastery("Blue Bottle", "San Francisco", "123-456-7890");
            network.AddRoastery(roastery);
            Assert.Single(network.Roasteries);
            Assert.Equal(roastery, network.Roasteries[0]);
        }

        [Fact]
        public void TestAddCafe()
        {
            var network = new DistributionNetwork();
            var cafe = new Cafe("Starbucks", "New York", "123-456-7890");
            network.AddCafe(cafe);
            Assert.Single(network.Cafes);
            Assert.Equal(cafe, network.Cafes[0]);
        }

        [Fact]
        public void TestSetShippingCostFromSupplierToRoastery()
        {
            var network = new DistributionNetwork();
            var supplier = new Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
            var roastery = new Roastery("Blue Bottle", "San Francisco", "123-456-7890");
            network.AddSupplier(supplier);
            network.AddRoastery(roastery);
            network.SetShippingCostFromSupplierToRoastery(supplier, roastery, 50);
            Assert.Single(network.ShippingCostFromSupplierToRoastery);
            Assert.Equal(50, network.ShippingCostFromSupplierToRoastery[(supplier, roastery)]);
        }

        [Fact]
        public void TestSetShippingCostFromRoasteryToCafe()
        {
            var network = new DistributionNetwork();
            var roastery = new Roastery("Blue Bottle", "San Francisco", "123-456-7890");
            var cafe = new Cafe("Starbucks", "New York", "123-456-7890");
            network.AddRoastery(roastery);
            network.AddCafe(cafe);
            network.SetShippingCostFromRoasteryToCafe(roastery, cafe, 100);
            Assert.Single(network.ShippingCostFromRoasteryToCafe);
            Assert.Equal(100, network.ShippingCostFromRoasteryToCafe[(roastery, cafe)]);
        }
    }
}