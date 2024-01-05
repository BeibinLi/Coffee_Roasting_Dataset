import tech.tablesaw.api.Table;
import tech.tablesaw.plotly.Plot;
import tech.tablesaw.plotly.api.BarPlot;
import tech.tablesaw.plotly.components.Figure;
import tech.tablesaw.plotly.components.Layout;

import java.io.IOException;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;

public class MembershipDuration {

    public static void main(String[] args) throws IOException {
        Map<String, Integer> membershipCounts = getMembershipCounts("database/customer.csv");
        plot(membershipCounts);
    }

    private static Map<String, Integer> getMembershipCounts(String filePath) throws IOException {
        Table table = Table.read().csv(filePath);
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        Map<String, Integer> membershipCounts = new HashMap<>();

        for (String dateStr : table.stringColumn("member_since")) {
            LocalDate date = LocalDate.parse(dateStr, formatter);
            String yearMonth = date.getYear() + "-" + date.getMonthValue();
            membershipCounts.put(yearMonth, membershipCounts.getOrDefault(yearMonth, 0) + 1);
        }

        return membershipCounts;
    }

    private static void plot(Map<String, Integer> membershipCounts) {
        String[] categories = membershipCounts.keySet().toArray(new String[0]);
        int[] values = membershipCounts.values().stream().mapToInt(Integer::intValue).toArray();

        Figure figure = BarPlot.create("Duration of Membership (Monthly)", categories, "Year-Month", values);
        Layout layout = figure.getLayout().toBuilder()
                .xAxis(figure.getLayout().xAxis().toBuilder().tickAngle(45).build())
                .build();
        figure = figure.toBuilder().layout(layout).build();

        Plot.show(figure);
    }
}