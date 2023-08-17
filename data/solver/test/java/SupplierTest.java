import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class SupplierTest {

    @Test
    void testSupplierInit() {
        Supplier supplier = new Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
        assertEquals("Coffee Bean Co.", supplier.getName());
        assertEquals(1000, supplier.getCapacity());
        assertEquals("Seattle", supplier.getLocation());
        assertEquals("123-456-7890", supplier.getContact());
        assertTrue(supplier.getShippingCosts().isEmpty());
    }

    @Test
    void testSetShippingCost() {
        Supplier supplier = new Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
        supplier.setShippingCost("Roastery A", 50);
        assertEquals(1, supplier.getShippingCosts().size());
        assertEquals(50, supplier.getShippingCosts().get("Roastery A"));
    }

    @Test
    void testGetShippingCost() {
        Supplier supplier = new Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
        supplier.setShippingCost("Roastery A", 50);
        assertEquals(50, supplier.getShippingCost("Roastery A"));
        assertEquals(Double.POSITIVE_INFINITY, supplier.getShippingCost("Roastery B"));
    }

    @Test
    void testToString() {
        Supplier supplier = new Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
        assertEquals("Supplier(name=Coffee Bean Co., capacity=1000, location=Seattle, contact=123-456-7890)", supplier.toString());
    }

    @Test
    void testValidateCapacity() {
        Supplier supplier = new Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
        assertTrue(supplier.validateCapacity(500));
        assertFalse(supplier.validateCapacity(1500));
    }
}