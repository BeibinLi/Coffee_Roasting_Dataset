using System;
using System.IO;
using System.Data;
using System.Drawing;
using System.Linq;
using ScottPlot;

namespace CoffeeDistribution.Visualization
{
    public class BeanPricePlot
    {
        public static DataTable GetData(DataTable dataTable, string beanName)
        {
            var filteredData = dataTable.AsEnumerable()
                .Where(row => row.Field<string>("source_bean_type").ToLower() == beanName.ToLower())
                .CopyToDataTable();

            if (filteredData.Rows.Count == 0)
            {
                throw new ArgumentException($"No bean with name {beanName} found.");
            }

            foreach (DataRow row in filteredData.Rows)
            {
                row.SetField("date", new DateTime(row.Field<int>("year"), row.Field<int>("month"), 1));
            }

            return filteredData;
        }

        public static void PlotData(DataTable data, string beanName)
        {
            var plt = new Plot(800, 400);

            var groupedData = data.AsEnumerable()
                .GroupBy(row => row.Field<DateTime>("date"))
                .Select(group => new
                {
                    Date = group.Key,
                    Min = group.Min(row => row.Field<double>("price_per_unit")),
                    Max = group.Max(row => row.Field<double>("price_per_unit")),
                    Mean = group.Average(row => row.Field<double>("price_per_unit"))
                })
                .OrderBy(x => x.Date)
                .ToList();

            var dates = groupedData.Select(x => x.Date.ToOADate()).ToArray();
            var minPrices = groupedData.Select(x => x.Min).ToArray();
            var maxPrices = groupedData.Select(x => x.Max).ToArray();
            var meanPrices = groupedData.Select(x => x.Mean).ToArray();

            plt.PlotFill(dates, minPrices, maxPrices, fillColor: Color.FromArgb(100, 135, 206, 250), label: "Price Range (Min to Max)");
            plt.PlotScatter(dates, meanPrices, color: Color.Blue, markerSize: 5, label: "Mean Price");

            plt.Title($"Bean Price Chart for {beanName}");
            plt.XLabel("Time");
            plt.YLabel("Price");
            plt.Legend();
            plt.Ticks(dateTimeX: true);
            plt.Grid(lineStyle: LineStyle.Dash);

            Directory.CreateDirectory("images");
            plt.SaveFig($"images/bean_price_{beanName}.png");
        }
    }
}