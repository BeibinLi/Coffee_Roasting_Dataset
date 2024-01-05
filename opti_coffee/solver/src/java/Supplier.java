import java.util.HashMap;
import java.util.Map;

public class Supplier {
    private String name;
    private int capacity;
    private String location;
    private String contact;
    private Map<String, Integer> shippingCosts;

    public Supplier(String name, int capacity, String location, String contact) {
        this.name = name;
        this.capacity = capacity;
        this.location = location;
        this.contact = contact;
        this.shippingCosts = new HashMap<>();
    }

    public void setShippingCost(String roasteryName, int cost) {
        this.shippingCosts.put(roasteryName, cost);
    }

    public int getShippingCost(String roasteryName) {
        return this.shippingCosts.getOrDefault(roasteryName, Integer.MAX_VALUE);
    }

    @Override
    public String toString() {
        return "Supplier(name=" + this.name + ", capacity=" + this.capacity + ", location=" + this.location + ", contact=" + this.contact + ")";
    }

    public boolean validateCapacity(int requestedQuantity) {
        return requestedQuantity <= this.capacity;
    }

    public void reduceCapacity(int quantity) {
        if (validateCapacity(quantity)) {
            this.capacity -= quantity;
        } else {
            throw new IllegalArgumentException("Requested quantity exceeds capacity");
        }
    }

    public void increaseCapacity(int quantity) {
        this.capacity += quantity;
    }

    public String displayInfo() {
        StringBuilder info = new StringBuilder();
        info.append("Name: ").append(this.name).append("\n");
        info.append("Capacity: ").append(this.capacity).append("\n");
        info.append("Location: ").append(this.location).append("\n");
        info.append("Contact: ").append(this.contact).append("\n");
        info.append("Shipping Costs:\n");
        for (Map.Entry<String, Integer> entry : this.shippingCosts.entrySet()) {
            info.append("  - ").append(entry.getKey()).append(": ").append(entry.getValue()).append("\n");
        }
        return info.toString();
    }

    // Getters and setters for name, capacity, location, and contact
}