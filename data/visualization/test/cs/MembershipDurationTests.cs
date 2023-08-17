using Xunit;
using CoffeeDistribution.Visualization;
using System.Data;

namespace CoffeeDistribution.Tests
{
    public class MembershipDurationTests
    {
        [Fact]
        public void TestGetData()
        {
            // Create a sample DataTable with membership data
            var data = new DataTable();
            data.Columns.Add("member_since", typeof(string));
            data.Columns.Add("customer_id", typeof(int));
            data.Rows.Add("2021-01-01", 1);
            data.Rows.Add("2021-01-02", 2);
            data.Rows.Add("2021-02-01", 3);
            data.Rows.Add("2021-02-02", 4);
            data.Rows.Add("2021-03-01", 5);

            // Test the GetData function with the sample DataTable
            var output = MembershipDurationPlot.GetData(data);

            // Check if the output matches the expected result
            Assert.Equal(3, output.Rows.Count);
            Assert.Equal("2021-01", output.Rows[0].Field<string>("MembershipYearMonth"));
            Assert.Equal(2, output.Rows[0].Field<int>("Count"));
            Assert.Equal("2021-02", output.Rows[1].Field<string>("MembershipYearMonth"));
            Assert.Equal(2, output.Rows[1].Field<int>("Count"));
            Assert.Equal("2021-03", output.Rows[2].Field<string>("MembershipYearMonth"));
            Assert.Equal(1, output.Rows[2].Field<int>("Count"));
        }
    }
}