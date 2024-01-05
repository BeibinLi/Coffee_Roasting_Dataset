using Xunit;
using CoffeeDistribution.Entities;

namespace CoffeeDistribution.Tests
{
    public class CafeTests
    {
        [Fact]
        public void TestCafeInit()
        {
            var cafe = new Cafe("Starbucks", "New York", "123-456-7890");
            Assert.Equal("Starbucks", cafe.Name);
            Assert.Equal("New York", cafe.Location);
            Assert.Equal("123-456-7890", cafe.Contact);
            Assert.Empty(cafe.CoffeeDemand);
        }

        [Fact]
        public void TestSetCoffeeDemand()
        {
            var cafe = new Cafe("Starbucks", "New York", "123-456-7890");
            cafe.SetCoffeeDemand("Cold Brew", 10);
            Assert.Single(cafe.CoffeeDemand);
            Assert.Equal(10, cafe.CoffeeDemand["Cold Brew"]);
        }

        [Fact]
        public void TestGetCoffeeDemand()
        {
            var cafe = new Cafe("Starbucks", "New York", "123-456-7890");
            cafe.SetCoffeeDemand("Cold Brew", 10);
            Assert.Equal(10, cafe.GetCoffeeDemand("Cold Brew"));
            Assert.Equal(0, cafe.GetCoffeeDemand("Espresso"));
        }

        [Fact]
        public void TestDisplayInfo()
        {
            var cafe = new Cafe("Starbucks", "New York", "123-456-7890");
            cafe.SetCoffeeDemand("Cold Brew", 10);
            string expectedOutput = "Name: Starbucks\nLocation: New York\nContact: 123-456-7890\nCoffee Demand:\n  - Cold Brew: 10\n";
            Assert.Equal(expectedOutput, cafe.DisplayInfo());
        }

        [Fact]
        public void TestToString()
        {
            var cafe = new Cafe("Starbucks", "New York", "123-456-7890");
            Assert.Equal("Cafe(name=Starbucks, location=New York, contact=123-456-7890)", cafe.ToString());
        }
    }
}