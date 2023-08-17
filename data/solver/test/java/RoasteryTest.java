import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class RoasteryTest {

    @Test
    void testRoasteryInit() {
        Roastery roastery = new Roastery("Blue Bottle", "San Francisco", "123-456-7890");
        assertEquals("Blue Bottle", roastery.getName());
        assertEquals("San Francisco", roastery.getLocation());
        assertEquals("123-456-7890", roastery.getContact());
        assertTrue(roastery.getRoastingCosts().isEmpty());
        assertTrue(roastery.getShippingCosts().isEmpty());
    }

    @Test
    void testSetRoastingCost() {
        Roastery roastery = new Roastery("Blue Bottle", "San Francisco", "123-456-7890");
        roastery.setRoastingCost("Cold Brew", 50, "Robusta beans only");
        assertEquals(1, roastery.getRoastingCosts().size());
        assertEquals(50, roastery.getRoastingCosts().get("Cold Brew").getCost());
        assertEquals("Robusta beans only", roastery.getRoastingCosts().get("Cold Brew").getConstraints());
    }

    @Test
    void testSetShippingCost() {
        Roastery roastery = new Roastery("Blue Bottle", "San Francisco", "123-456-7890");
        roastery.setShippingCost("Starbucks", 100);
        assertEquals(1, roastery.getShippingCosts().size());
        assertEquals(100, roastery.getShippingCosts().get("Starbucks"));
    }

    @Test
    void testGetShippingCost() {
        Roastery roastery = new Roastery("Blue Bottle", "San Francisco", "123-456-7890");
        roastery.setShippingCost("Starbucks", 100);
        assertEquals(100, roastery.getShippingCost("Starbucks"));
        assertEquals(Double.POSITIVE_INFINITY, roastery.getShippingCost("Peet's Coffee"));
    }

    @Test
    void testGetRoastingCost() {
        Roastery roastery = new Roastery("Blue Bottle", "San Francisco", "123-456-7890");
        roastery.setRoastingCost("Cold Brew", 50, "Robusta beans only");
        assertEquals(50, roastery.getRoastingCost("Cold Brew"));
        assertEquals(Double.POSITIVE_INFINITY, roastery.getRoastingCost("Espresso"));
    }
}