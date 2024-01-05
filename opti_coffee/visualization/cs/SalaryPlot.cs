using System;
using System.IO;
using System.Linq;
using OxyPlot;
using OxyPlot.Axes;
using OxyPlot.Series;
using System.Collections.Generic;
using System.Data;

namespace CoffeeDistribution.Visualization
{
    public class SalaryPlot
    {
        public static void Plot(DataTable dataTable, int salaryQuantum)
        {
            var minSalary = (int)dataTable.AsEnumerable().Min(row => row.Field<int>("salary")) / salaryQuantum * salaryQuantum;
            var maxSalary = ((int)dataTable.AsEnumerable().Max(row => row.Field<int>("salary")) + salaryQuantum - 1) / salaryQuantum * salaryQuantum;

            var model = new PlotModel { Title = "Distribution of Salaries" };

            var histogram = new HistogramSeries
            {
                StrokeThickness = 1,
                StrokeColor = OxyColors.Black,
                FillColor = OxyColor.FromRgb(135, 206, 250),
                BinWidth = salaryQuantum
            };

            foreach (DataRow row in dataTable.Rows)
            {
                histogram.Items.Add(new HistogramItem(row.Field<int>("salary"), row.Field<int>("salary") + salaryQuantum, 1));
            }

            model.Series.Add(histogram);

            model.Axes.Add(new LinearAxis { Position = AxisPosition.Bottom, Title = "Salary Amount" });
            model.Axes.Add(new LinearAxis { Position = AxisPosition.Left, Title = "Frequency" });

            Directory.CreateDirectory("images");
            using (var stream = File.Create("images/salary.png"))
            {
                var pngExporter = new OxyPlot.Wpf.PngExporter { Width = 600, Height = 400, Background = OxyColors.White };
                pngExporter.Export(model, stream);
            }
        }
    }
}