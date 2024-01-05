using System;
using System.IO;
using System.Data;
using System.Drawing;
using System.Linq;
using ScottPlot;

namespace CoffeeDistribution.Visualization
{
    public class SupplierPricePlot
    {
        public static int GetSupplierId(int? supplierId, string supplierName, DataTable suppliers)
        {
            if (supplierId == null && supplierName == null)
            {
                throw new ArgumentException("Either supplierId or supplierName must be specified.");
            }

            if (supplierId == null)
            {
                var rows = suppliers.AsEnumerable().Where(row => row.Field<string>("contact_name") == supplierName).ToList();

                if (rows.Count == 0)
                {
                    throw new ArgumentException($"No supplier with name {supplierName} found.");
                }
                else if (rows.Count > 1)
                {
                    throw new ArgumentException($"Multiple suppliers with name {supplierName} found.");
                }

                supplierId = rows[0].Field<int>("supplier_id");
            }

            return supplierId.Value;
        }

        public static DataTable GetData(int supplierId, DataTable dataTable)
        {
            var filteredData = dataTable.AsEnumerable().Where(row => row.Field<int>("supplier_id") == supplierId).CopyToDataTable();

            foreach (DataRow row in filteredData.Rows)
            {
                row.SetField("date", new DateTime(row.Field<int>("year"), row.Field<int>("month"), 1));
            }

            return filteredData;
        }

        public static void Plot(DataTable filteredData, int supplierId)
        {
            var plt = new Plot(800, 400);

            var dates = filteredData.AsEnumerable().Select(row => row.Field<DateTime>("date").ToOADate()).ToArray();
            var prices = filteredData.AsEnumerable().Select(row => row.Field<double>("price_per_unit")).ToArray();

            plt.PlotScatter(dates, prices, color: Color.Blue, markerSize: 5, label: $"Supplier {supplierId}");
            plt.Title($"Change in Supply Price for Supplier {supplierId}");
            plt.XLabel("Date");
            plt.YLabel("Price per Unit");
            plt.Ticks(dateTimeX: true);
            plt.Grid(lineStyle: LineStyle.Dash);

            Directory.CreateDirectory("images");
            plt.SaveFig($"images/supplier_price_{supplierId}.png");
        }
    }
}