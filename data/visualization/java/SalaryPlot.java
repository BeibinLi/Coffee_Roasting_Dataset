import org.knowm.xchart.CategoryChart;
import org.knowm.xchart.CategoryChartBuilder;
import org.knowm.xchart.SwingWrapper;
import org.knowm.xchart.style.Styler;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SalaryPlot {

    public static void main(String[] args) {
        List<Integer> salaries = readSalariesFromCSV("database/employee.csv");
        plot(salaries, 1000);
    }

    private static List<Integer> readSalariesFromCSV(String filePath) {
        List<Integer> salaries = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            boolean isFirstLine = true;
            while ((line = br.readLine()) != null) {
                if (isFirstLine) {
                    isFirstLine = false;
                    continue;
                }
                String[] values = line.split(",");
                salaries.add(Integer.parseInt(values[3])); // Assuming salary is in the 4th column
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return salaries;
    }

    private static void plot(List<Integer> salaries, int salaryQuantum) {
        int minSalary = salaries.stream().min(Integer::compare).orElse(0) / salaryQuantum * salaryQuantum;
        int maxSalary = (salaries.stream().max(Integer::compare).orElse(0) + salaryQuantum - 1) / salaryQuantum * salaryQuantum;

        Map<String, Integer> histogram = new HashMap<>();
        for (int salary : salaries) {
            int bin = salary / salaryQuantum * salaryQuantum;
            histogram.put(Integer.toString(bin), histogram.getOrDefault(Integer.toString(bin), 0) + 1);
        }

        CategoryChart chart = new CategoryChartBuilder()
                .width(800)
                .height(600)
                .title("Distribution of Salaries")
                .xAxisTitle("Salary Amount")
                .yAxisTitle("Frequency")
                .build();

        chart.getStyler().setLegendVisible(false);
        chart.getStyler().setHasAnnotations(true);
        chart.getStyler().setXAxisLabelRotation(90);
        chart.getStyler().setYAxisLabelAlignment(Styler.TextAlignment.Right);
        chart.getStyler().setYAxisLabelPosition(Styler.YAxisLabelPosition.Inside);
        chart.getStyler().setPlotGridLinesVisible(false);

        chart.addSeries("Frequency", new ArrayList<>(histogram.keySet()), new ArrayList<>(histogram.values()));

        new SwingWrapper<>(chart).displayChart();
    }
}