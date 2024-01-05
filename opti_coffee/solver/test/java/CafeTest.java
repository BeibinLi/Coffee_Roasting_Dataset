import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CafeTest {

    @Test
    void testCafeInit() {
        Cafe cafe = new Cafe("Starbucks", "New York", "123-456-7890");
        assertEquals("Starbucks", cafe.getName());
        assertEquals("New York", cafe.getLocation());
        assertEquals("123-456-7890", cafe.getContact());
        assertTrue(cafe.getCoffeeDemand().isEmpty());
    }

    @Test
    void testSetCoffeeDemand() {
        Cafe cafe = new Cafe("Starbucks", "New York", "123-456-7890");
        cafe.setCoffeeDemand("Cold Brew", 10);
        assertEquals(1, cafe.getCoffeeDemand().size());
        assertEquals(10, cafe.getCoffeeDemand().get("Cold Brew"));
    }

    @Test
    void testGetCoffeeDemand() {
        Cafe cafe = new Cafe("Starbucks", "New York", "123-456-7890");
        cafe.setCoffeeDemand("Cold Brew", 10);
        assertEquals(10, cafe.getCoffeeDemand("Cold Brew"));
        assertEquals(0, cafe.getCoffeeDemand("Espresso"));
    }

    @Test
    void testDisplayInfo() {
        Cafe cafe = new Cafe("Starbucks", "New York", "123-456-7890");
        cafe.setCoffeeDemand("Cold Brew", 10);
        String expectedOutput = "Name: Starbucks\nLocation: New York\nContact: 123-456-7890\nCoffee Demand:\n  - Cold Brew: 10\n";
        assertEquals(expectedOutput, cafe.displayInfo());
    }

    @Test
    void testToString() {
        Cafe cafe = new Cafe("Starbucks", "New York", "123-456-7890");
        assertEquals("Cafe(name=Starbucks, location=New York, contact=123-456-7890)", cafe.toString());
    }
}