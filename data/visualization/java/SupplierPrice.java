import tech.tablesaw.api.DateTimeColumn;
import tech.tablesaw.api.DoubleColumn;
import tech.tablesaw.api.Table;
import tech.tablesaw.plotly.Plot;
import tech.tablesaw.plotly.api.LinePlot;
import tech.tablesaw.plotly.components.Figure;
import tech.tablesaw.plotly.components.Layout;

import java.io.IOException;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;

public class SupplierPrice {

    public static void main(String[] args) throws IOException {
        int supplierId = args.length > 0 ? Integer.parseInt(args[0]) : 1;
        Table data = getData(supplierId);
        plotData(data, supplierId);
    }

    private static Table getData(int supplierId) throws IOException {
        Table table = Table.read().csv("database/supply_price_history.csv");
        table = table.where(table.intColumn("supplier_id").isEqualTo(supplierId));

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        DateTimeColumn dateColumn = table.dateColumn("year").asYearMonthDayColumn().asLocalDateColumn().map(date -> {
            int year = date.getYear();
            int month = date.getMonthValue();
            return LocalDate.parse(year + "-" + month + "-01", formatter);
        }).setName("date");

        table.addColumns(dateColumn);
        return table;
    }

    private static void plotData(Table data, int supplierId) {
        DateTimeColumn dateColumn = data.dateTimeColumn("date");
        DoubleColumn priceColumn = data.doubleColumn("price_per_unit");

        Figure figure = LinePlot.create("Change in Supply Price for Supplier " + supplierId,
                dateColumn, priceColumn);
        Layout layout = figure.getLayout().toBuilder()
                .yAxis(figure.getLayout().yAxis().toBuilder().gridWidth(0.5).build())
                .xAxis(figure.getLayout().xAxis().toBuilder().gridWidth(0.5).build())
                .build();
        figure = figure.toBuilder().layout(layout).build();

        Plot.show(figure);
    }
}