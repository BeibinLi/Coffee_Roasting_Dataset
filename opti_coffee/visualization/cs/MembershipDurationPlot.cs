using System;
using System.IO;
using System.Data;
using System.Drawing;
using System.Linq;
using ScottPlot;

namespace CoffeeDistribution.Visualization
{
    public class MembershipDurationPlot
    {
        public static DataTable GetData(DataTable dataTable)
        {
            var membershipCounts = new DataTable();
            membershipCounts.Columns.Add("MembershipYearMonth", typeof(DateTime));
            membershipCounts.Columns.Add("Count", typeof(int));

            var groupedData = dataTable.AsEnumerable()
                .GroupBy(row => row.Field<DateTime>("member_since").ToString("yyyy-MM"))
                .Select(group => new { MembershipYearMonth = DateTime.Parse(group.Key), Count = group.Count() })
                .OrderBy(x => x.MembershipYearMonth);

            foreach (var group in groupedData)
            {
                membershipCounts.Rows.Add(group.MembershipYearMonth, group.Count);
            }

            return membershipCounts;
        }

        public static void Plot(DataTable membershipCounts)
        {
            var plt = new Plot(800, 400);

            var barData = membershipCounts.AsEnumerable().Select(row => row.Field<int>("Count")).ToArray();
            var barLabels = membershipCounts.AsEnumerable().Select(row => row.Field<DateTime>("MembershipYearMonth").ToString("yyyy-MM")).ToArray();

            plt.PlotBar(barData, barLabels, fillColor: Color.SkyBlue);
            plt.Title("Duration of Membership (Monthly)");
            plt.XLabel("Year-Month");
            plt.YLabel("Number of Customers Joined");
            plt.Ticks(dateTimeX: true, rotateX: 45);

            Directory.CreateDirectory("images");
            plt.SaveFig("images/membership_duration.png");
        }
    }
}