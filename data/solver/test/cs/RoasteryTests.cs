using Xunit;
using CoffeeDistribution.Entities;

namespace CoffeeDistribution.Tests
{
    public class RoasteryTests
    {
        [Fact]
        public void TestRoasteryInit()
        {
            var roastery = new Roastery("Blue Bottle", "San Francisco", "123-456-7890");
            Assert.Equal("Blue Bottle", roastery.Name);
            Assert.Equal("San Francisco", roastery.Location);
            Assert.Equal("123-456-7890", roastery.Contact);
            Assert.Empty(roastery.RoastingCosts);
            Assert.Empty(roastery.ShippingCosts);
        }

        [Fact]
        public void TestSetRoastingCost()
        {
            var roastery = new Roastery("Blue Bottle", "San Francisco", "123-456-7890");
            roastery.SetRoastingCost("Cold Brew", 50, "Robusta beans only");
            Assert.Single(roastery.RoastingCosts);
            Assert.Equal(50, roastery.RoastingCosts["Cold Brew"].Cost);
            Assert.Equal("Robusta beans only", roastery.RoastingCosts["Cold Brew"].Constraints);
        }

        [Fact]
        public void TestSetShippingCost()
        {
            var roastery = new Roastery("Blue Bottle", "San Francisco", "123-456-7890");
            roastery.SetShippingCost("Starbucks", 100);
            Assert.Single(roastery.ShippingCosts);
            Assert.Equal(100, roastery.ShippingCosts["Starbucks"]);
        }

        [Fact]
        public void TestGetShippingCost()
        {
            var roastery = new Roastery("Blue Bottle", "San Francisco", "123-456-7890");
            roastery.SetShippingCost("Starbucks", 100);
            Assert.Equal(100, roastery.GetShippingCost("Starbucks"));
            Assert.Equal(double.PositiveInfinity, roastery.GetShippingCost("Peet's Coffee"));
        }

        [Fact]
        public void TestGetRoastingCost()
        {
            var roastery = new Roastery("Blue Bottle", "San Francisco", "123-456-7890");
            roastery.SetRoastingCost("Cold Brew", 50, "Robusta beans only");
            Assert.Equal(50, roastery.GetRoastingCost("Cold Brew"));
            Assert.Equal(double.PositiveInfinity, roastery.GetRoastingCost("Espresso"));
        }
    }
}