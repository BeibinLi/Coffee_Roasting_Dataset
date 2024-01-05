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

public class BeanPrice {

    public static void main(String[] args) throws IOException {
        String beanName = args.length > 0 ? args[0].toLowerCase() : "arabica";
        Table data = getData(beanName);
        plotData(data, beanName);
    }

    private static Table getData(String beanName) throws IOException {
        Table table = Table.read().csv("database/sell_price_history.csv");
        table = table.where(table.stringColumn("source_bean_type").isEqualToIgnoringCase(beanName));

        if (table.isEmpty()) {
            throw new IllegalArgumentException("No bean with name " + beanName + " found.");
        }

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        DateTimeColumn dateColumn = table.dateColumn("year").asYearMonthDayColumn().asLocalDateColumn().map(date -> {
            int year = date.getYear();
            int month = date.getMonthValue();
            return LocalDate.parse(year + "-" + month + "-01", formatter);
        }).setName("date");

        table.addColumns(dateColumn);
        return table;
    }

    private static void plotData(Table data, String beanName) {
        DateTimeColumn dateColumn = data.dateTimeColumn("date");
        DoubleColumn minColumn = data.doubleColumn("price_per_unit").minByDate(dateColumn);
        DoubleColumn maxColumn = data.doubleColumn("price_per_unit").maxByDate(dateColumn);
        DoubleColumn meanColumn = data.doubleColumn("price_per_unit").meanByDate(dateColumn);

        Figure figure = LinePlot.create(beanName + " Bean Price Chart",
                dateColumn, minColumn, maxColumn, meanColumn);
        Layout layout = figure.getLayout().toBuilder()
                .yAxis(figure.getLayout().yAxis().toBuilder().gridWidth(0.5).build())
                .xAxis(figure.getLayout().xAxis().toBuilder().gridWidth(0.5).build())
                .build();
        figure = figure.toBuilder().layout(layout).build();

        Plot.show(figure);
    }
}