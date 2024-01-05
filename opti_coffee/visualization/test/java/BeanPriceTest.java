import org.junit.jupiter.api.Test;
import tech.tablesaw.api.DateTimeColumn;
import tech.tablesaw.api.DoubleColumn;
import tech.tablesaw.api.Table;
import java.io.File;
import java.time.LocalDate;
import static org.junit.jupiter.api.Assertions.*;

class BeanPriceTest {

    @Test
    void testPlotData() {
        // Create a sample Table with bean price data
        Table data = Table.create("bean_price_data")
                .addColumns(
                        DateTimeColumn.create("date", LocalDate.of(2021, 1, 1), LocalDate.of(2021, 1, 2), LocalDate.of(2021, 1, 3)),
                        DoubleColumn.create("min", 5, 6, 7),
                        DoubleColumn.create("max", 10, 12, 14),
                        DoubleColumn.create("mean", 7.5, 9, 10.5)
                );
        String beanName = "arabica";

        // Test the plotData function with the sample Table
        BeanPrice.plotData(data, beanName);

        // Check that the image file was created
        assertTrue(new File("images/bean_price_" + beanName + ".png").exists());
    }
}