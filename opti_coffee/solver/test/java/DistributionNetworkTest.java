import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class DistributionNetworkTest {

    @Test
    void testAddSupplier() {
        DistributionNetwork network = new DistributionNetwork();
        Supplier supplier = new Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
        network.addSupplier(supplier);
        assertEquals(1, network.getSuppliers().size());
        assertEquals(supplier, network.getSuppliers().get(0));
    }

    @Test
    void testAddRoastery() {
        DistributionNetwork network = new DistributionNetwork();
        Roastery roastery = new Roastery("Blue Bottle", "San Francisco", "123-456-7890");
        network.addRoastery(roastery);
        assertEquals(1, network.getRoasteries().size());
        assertEquals(roastery, network.getRoasteries().get(0));
    }

    @Test
    void testAddCafe() {
        DistributionNetwork network = new DistributionNetwork();
        Cafe cafe = new Cafe("Starbucks", "New York", "123-456-7890");
        network.addCafe(cafe);
        assertEquals(1, network.getCafes().size());
        assertEquals(cafe, network.getCafes().get(0));
    }

    @Test
    void testSetShippingCostFromSupplierToRoastery() {
        DistributionNetwork network = new DistributionNetwork();
        Supplier supplier = new Supplier("Coffee Bean Co.", 1000, "Seattle", "123-456-7890");
        Roastery roastery = new Roastery("Blue Bottle", "San Francisco", "123-456-7890");
        network.addSupplier(supplier);
        network.addRoastery(roastery);
        network.setShippingCostFromSupplierToRoastery(supplier, roastery, 50);
        assertEquals(1, network.getShippingCostFromSupplierToRoastery().size());
        assertEquals(50, network.getShippingCostFromSupplierToRoastery().get(supplier, roastery));
    }

    @Test
    void testSetShippingCostFromRoasteryToCafe() {
        DistributionNetwork network = new DistributionNetwork();
        Roastery roastery = new Roastery("Blue Bottle", "San Francisco", "123-456-7890");
        Cafe cafe = new Cafe("Starbucks", "New York", "123-456-7890");
        network.addRoastery(roastery);
        network.addCafe(cafe);
        network.setShippingCostFromRoasteryToCafe(roastery, cafe, 100);
        assertEquals(1, network.getShippingCostFromRoasteryToCafe().size());
        assertEquals(100, network.getShippingCostFromRoasteryToCafe().get(roastery, cafe));
    }
}