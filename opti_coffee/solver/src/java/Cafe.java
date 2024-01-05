import java.util.HashMap;
import java.util.Map;

public class Cafe {
    private String name;
    private String location;
    private String contact;
    private Map<String, Integer> coffeeDemand;

    public Cafe(String name, String location, String contact) {
        this.name = name;
        this.location = location;
        this.contact = contact;
        this.coffeeDemand = new HashMap<>();
    }

    public void setCoffeeDemand(String coffeeType, int quantity) {
        this.coffeeDemand.put(coffeeType, quantity);
    }

    public int getCoffeeDemand(String coffeeType) {
        return this.coffeeDemand.getOrDefault(coffeeType, 0);
    }

    public String displayInfo() {
        StringBuilder info = new StringBuilder();
        info.append("Name: ").append(this.name).append("\n");
        info.append("Location: ").append(this.location).append("\n");
        info.append("Contact: ").append(this.contact).append("\n");
        info.append("Coffee Demand:\n");
        for (Map.Entry<String, Integer> entry : this.coffeeDemand.entrySet()) {
            info.append("  - ").append(entry.getKey()).append(": ").append(entry.getValue()).append("\n");
        }
        return info.toString();
    }

    @Override
    public String toString() {
        return "Cafe(name=" + this.name + ", location=" + this.location + ", contact=" + this.contact + ")";
    }

    public void fulfillDemand(String coffeeType, int quantity) {
        int currentDemand = getCoffeeDemand(coffeeType);
        if (quantity > currentDemand) {
            throw new IllegalArgumentException("Fulfilled quantity exceeds demand");
        }
        this.coffeeDemand.put(coffeeType, currentDemand - quantity);
    }

    // Getters and setters for name, location, and contact
}