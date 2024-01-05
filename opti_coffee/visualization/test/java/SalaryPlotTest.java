import org.junit.jupiter.api.Test;
import tech.tablesaw.api.Table;
import java.io.File;
import static org.junit.jupiter.api.Assertions.*;

class SalaryPlotTest {

    @Test
    void testPlot() {
        // Create a sample Table with salary data
        Table data = Table.create("salary_data")
                .addColumns(
                        Table.intColumn("employee_id", 1, 2, 3, 4, 5),
                        Table.intColumn("salary", 50000, 60000, 70000, 80000, 90000)
                );
        int salaryQuantum = 10000;

        // Test the plot function with the sample Table
        SalaryPlot.plot(data, salaryQuantum);

        // Check that the image file was created
        assertTrue(new File("images/salary.png").exists());
    }
}