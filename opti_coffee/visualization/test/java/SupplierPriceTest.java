import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class SupplierPriceTest {

    @Test
    void testGetSupplierId() {
        // Test the getSupplierId function with a sample supplier name
        String[] args = {"--name", "Acme Coffee"};
        int supplierId = SupplierPrice.getSupplierId(args);

        // Check that the supplier ID is correct
        assertEquals(1, supplierId);
    }
}