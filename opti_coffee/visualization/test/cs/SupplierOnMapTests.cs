using Xunit;
using CoffeeDistribution.Visualization;

namespace CoffeeDistribution.Tests
{
    public class SupplierOnMapTests
    {
        [Fact]
        public void TestGetCoordinates()
        {
            // Test the GetCoordinates function with a sample city and country
            string city = "Seattle";
            string country = "USA";
            (double lat, double lng) = SupplierOnMap.GetCoordinates(city, country);

            // Check that the latitude and longitude are within reasonable bounds
            Assert.True(lat > 47 && lat < 48);
            Assert.True(lng > -123 && lng < -122);
        }
    }
}