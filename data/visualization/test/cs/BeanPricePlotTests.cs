using Xunit;
using CoffeeDistribution.Visualization;
using System.Data;
using System.IO;

namespace CoffeeDistribution.Tests
{
    public class BeanPricePlotTests
    {
        [Fact]
        public void TestPlotData()
        {
            // Create a sample DataTable with bean price data
            var data = new DataTable();
            data.Columns.Add("date", typeof(DateTime));
            data.Columns.Add("min", typeof(double));
            data.Columns.Add("max", typeof(double));
            data.Columns.Add("mean", typeof(double));
            data.Rows.Add(new DateTime(2021, 1, 1), 5, 10, 7.5);
            data.Rows.Add(new DateTime(2021, 1, 2), 6, 12, 9);
            data.Rows.Add(new DateTime(2021, 1, 3), 7, 14, 10.5);

            string beanName = "arabica";

            // Test the PlotData function with the sample DataTable
            BeanPricePlot.PlotData(data, beanName);

            // Check that the image file was created
            Assert.True(File.Exists($"images/bean_price_{beanName}.png"));
        }
    }
}