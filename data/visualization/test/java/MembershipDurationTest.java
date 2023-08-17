import org.junit.jupiter.api.Test;
import tech.tablesaw.api.Table;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.*;

class MembershipDurationTest {

    @Test
    void testGetData() {
        // Create a sample Table with membership data
        Table data = Table.create("membership_data")
                .addColumns(
                        Table.dateColumn("member_since", "2021-01-01", "2021-01-02", "2021-02-01", "2021-02-02", "2021-03-01"),
                        Table.intColumn("customer_id", 1, 2, 3, 4, 5)
                );

        // Expected output
        Map<String, Integer> expectedOutput = Map.of(
                "2021-01", 2,
                "2021-02", 2,
                "2021-03", 1
        );

        // Test the getData function with the sample Table
        Map<String, Integer> output = MembershipDuration.getMembershipCounts(data);
        assertEquals(expectedOutput, output);
    }
}