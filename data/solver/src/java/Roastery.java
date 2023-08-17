import java.util.HashMap;
import java.util.Map;

public class Roastery {
    private String name;
    private String location;
    private String contact;
    private Map<String, RoastingDetails> roastingCosts;
    private Map<String, Integer> shippingCosts;

    public Roastery(String name, String location, String contact) {
        this.name = name;
        this.location = location;
        this.contact = contact;
        this.roastingCosts = new HashMap<>();
        this.shippingCosts = new HashMap<>();
    }

    public void setRoastingCost(String coffeeType, int cost, String constraints) {
        this.roastingCosts.put(coffeeType, new RoastingDetails(cost, constraints));
    }

    public void setShippingCost(String cafeName, int cost) {
        this.shippingCosts.put(cafeName, cost);
    }

    public int getShippingCost(String cafeName) {
        return this.shippingCosts.getOrDefault(cafeName, Integer.MAX_VALUE);
    }

    public int getRoastingCost(String coffeeType) {
        RoastingDetails details = this.roastingCosts.get(coffeeType);
        return details != null ? details.getCost() : Integer.MAX_VALUE;
    }

    public String getRoastingConstraints(String coffeeType) {
        RoastingDetails details = this.roastingCosts.get(coffeeType);
        return details != null ? details.getConstraints() : null;
    }

    public String displayInfo() {
        StringBuilder info = new StringBuilder();
        info.append("Name: ").append(this.name).append("\n");
        info.append("Location: ").append(this.location).append("\n");
        info.append("Contact: ").append(this.contact).append("\n");
        info.append("Roasting Costs:\n");
        for (Map.Entry<String, RoastingDetails> entry : this.roastingCosts.entrySet()) {
            info.append("  - ").append(entry.getKey()).append(": ").append(entry.getValue().getCost())
                .append(" (Constraints: ").append(entry.getValue().getConstraints()).append(")\n");
        }
        info.append("Shipping Costs:\n");
        for (Map.Entry<String, Integer> entry : this.shippingCosts.entrySet()) {
            info.append("  - ").append(entry.getKey()).append(": ").append(entry.getValue()).append("\n");
        }
        return info.toString();
    }

    public boolean validateRoastingConstraints(String coffeeType, String constraints) {
        String requiredConstraints = getRoastingConstraints(coffeeType);
        return requiredConstraints == null || requiredConstraints.equals(constraints);
    }

    @Override
    public String toString() {
        return "Roastery(name=" + this.name + ", location=" + this.location + ", contact=" + this.contact + ")";
    }

    // Getters and setters for name, location, and contact

    private static class RoastingDetails {
        private int cost;
        private String constraints;

        public RoastingDetails(int cost, String constraints) {
            this.cost = cost;
            this.constraints = constraints;
        }

        public int getCost() {
            return cost;
        }

        public String getConstraints() {
            return constraints;
        }
    }
}