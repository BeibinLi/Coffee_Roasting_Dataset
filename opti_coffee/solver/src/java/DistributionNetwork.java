import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class DistributionNetwork {
    private List<Supplier> suppliers;
    private List<Roastery> roasteries;
    private List<Cafe> cafes;
    private Map<String, Map<String, Integer>> shippingCostFromSupplierToRoastery;
    private Map<String, Map<String, Integer>> shippingCostFromRoasteryToCafe;

    public DistributionNetwork() {
        this.suppliers = new ArrayList<>();
        this.roasteries = new ArrayList<>();
        this.cafes = new ArrayList<>();
        this.shippingCostFromSupplierToRoastery = new HashMap<>();
        this.shippingCostFromRoasteryToCafe = new HashMap<>();
    }

    public void addSupplier(Supplier supplier) {
        this.suppliers.add(supplier);
    }

    public void addRoastery(Roastery roastery) {
        this.roasteries.add(roastery);
    }

    public void addCafe(Cafe cafe) {
        this.cafes.add(cafe);
    }

    public void setShippingCostFromSupplierToRoastery(Supplier supplier, Roastery roastery, int cost) {
        this.shippingCostFromSupplierToRoastery.computeIfAbsent(supplier.getName(), k -> new HashMap<>()).put(roastery.getName(), cost);
    }

    public void setShippingCostFromRoasteryToCafe(Roastery roastery, Cafe cafe, int cost) {
        this.shippingCostFromRoasteryToCafe.computeIfAbsent(roastery.getName(), k -> new HashMap<>()).put(cafe.getName(), cost);
    }

    public int getShippingCostFromSupplierToRoastery(String supplierName, String roasteryName) {
        return this.shippingCostFromSupplierToRoastery.getOrDefault(supplierName, new HashMap<>()).getOrDefault(roasteryName, Integer.MAX_VALUE);
    }

    public int getShippingCostFromRoasteryToCafe(String roasteryName, String cafeName) {
        return this.shippingCostFromRoasteryToCafe.getOrDefault(roasteryName, new HashMap<>()).getOrDefault(cafeName, Integer.MAX_VALUE);
    }

    public void displayNetworkInfo() {
        System.out.println("Suppliers:");
        for (Supplier supplier : this.suppliers) {
            System.out.println(supplier);
        }
        System.out.println("\nRoasteries:");
        for (Roastery roastery : this.roasteries) {
            System.out.println(roastery);
        }
        System.out.println("\nCafes:");
        for (Cafe cafe : this.cafes) {
            System.out.println(cafe);
        }
    }

    // Getters for suppliers, roasteries, and cafes
}