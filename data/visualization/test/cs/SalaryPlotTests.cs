using Xunit;
using CoffeeDistribution.Visualization;
using System.Data;
using System.IO;

namespace CoffeeDistribution.Tests
{
    public class SalaryPlotTests
    {
        [Fact]
        public void TestPlot()
        {
            // Create a sample DataTable with salary data
            var data = new DataTable();
            data.Columns.Add("employee_id", typeof(int));
            data.Columns.Add("salary", typeof(int));
            data.Rows.Add(1, 50000);
            data.Rows.Add(2, 60000);
            data.Rows.Add(3, 70000);
            data.Rows.Add(4, 80000);
            data.Rows.Add(5, 90000);

            int salaryQuantum = 10000;

            // Test the Plot function with the sample DataTable
            SalaryPlot.Plot(data, salaryQuantum);

            // Check that the image file was created
            Assert.True(File.Exists("images/salary.png"));
        }
    }
}