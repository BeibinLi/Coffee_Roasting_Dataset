import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import gurobi.GRB;

class CoffeeDistributionOptimizerTest {

    @Test
    void testCreateVariables() {
        DistributionNetwork network = new DistributionNetwork();
        CoffeeDistributionOptimizer optimizer = new CoffeeDistributionOptimizer(network);
        optimizer.createVariables();
        assertEquals(12, optimizer.getVariables().size());  // Assuming 2 suppliers, 2 roasteries, and 2 cafes
    }

    @Test
    void testSetObjective() {
        DistributionNetwork network = new DistributionNetwork();
        CoffeeDistributionOptimizer optimizer = new CoffeeDistributionOptimizer(network);
        optimizer.createVariables();
        optimizer.setObjective();
        assertEquals(GRB.MINIMIZE, optimizer.getModel().getObjective().getSense());
    }

    @Test
    void testAddConstraints() {
        DistributionNetwork network = new DistributionNetwork();
        CoffeeDistributionOptimizer optimizer = new CoffeeDistributionOptimizer(network);
        optimizer.createVariables();
        optimizer.setObjective();
        optimizer.addConstraints();
        assertEquals(12, optimizer.getModel().getConstrs().length);  // Assuming 2 suppliers, 2 roasteries, and 2 cafes
    }
}