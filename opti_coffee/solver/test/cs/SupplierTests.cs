using Xunit;
using CoffeeDistribution.Entities;

namespace CoffeeDistribution.Tests
{
    public class SupplierTests
    {
        [Fact]
        public void TestSupplierInit()
        {
            var supplier = new Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
            Assert.Equal("Coffee Bean Co.", supplier.Name);
            Assert.Equal(1000, supplier.Capacity);
            Assert.Equal("Seattle", supplier.Location);
            Assert.Equal("123-456-7890", supplier.Contact);
            Assert.Empty(supplier.ShippingCosts);
        }

        [Fact]
        public void TestSetShippingCost()
        {
            var supplier = new Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
            supplier.SetShippingCost("Roastery A", 50);
            Assert.Single(supplier.ShippingCosts);
            Assert.Equal(50, supplier.ShippingCosts["Roastery A"]);
        }

        [Fact]
        public void TestGetShippingCost()
        {
            var supplier = new Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
            supplier.SetShippingCost("Roastery A", 50);
            Assert.Equal(50, supplier.GetShippingCost("Roastery A"));
            Assert.Equal(double.PositiveInfinity, supplier.GetShippingCost("Roastery B"));
        }

        [Fact]
        public void TestToString()
        {
            var supplier = new Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
            Assert.Equal("Supplier(name=Coffee Bean Co., capacity=1000, location=Seattle, contact=123-456-7890)", supplier.ToString());
        }

        [Fact]
        public void TestValidateCapacity()
        {
            var supplier = new Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
            Assert.True(supplier.ValidateCapacity(500));
            Assert.False(supplier.ValidateCapacity(1500));
        }
    }
}