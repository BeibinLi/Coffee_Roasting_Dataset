using Xunit;
using CoffeeDistribution.Visualization;
using System.Data;

namespace CoffeeDistribution.Tests
{
    public class SupplierPriceTests
    {
        [Fact]
        public void TestGetSupplierId()
        {
            // Create a sample DataTable with supplier data
            var suppliers = new DataTable();
            suppliers.Columns.Add("supplier_id", typeof(int));
            suppliers.Columns.Add("contact_name", typeof(string));
            suppliers.Rows.Add(1, "Acme Coffee");

            // Test the GetSupplierId function with a sample supplier name
            int? supplierId = null;
            string supplierName = "Acme Coffee";
            int output = SupplierPricePlot.GetSupplierId(supplierId, supplierName, suppliers);

            // Check that the supplier ID is correct
            Assert.Equal(1, output);
        }
    }
}