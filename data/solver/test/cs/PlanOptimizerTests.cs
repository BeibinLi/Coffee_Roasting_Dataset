using Xunit;
using CoffeeDistribution.Entities;
using CoffeeDistribution.Optimizer;
using Gurobi;

namespace CoffeeDistribution.Tests
{
    public class PlanOptimizerTests
    {
        [Fact]
        public void TestCreateVariables()
        {
            var network = new DistributionNetwork();
            var optimizer = new CoffeeDistributionOptimizer(network);
            optimizer.CreateVariables();
            Assert.Equal(12, optimizer.Variables.Count);  // Assuming 2 suppliers, 2 roasteries, and 2 cafes
        }

        [Fact]
        public void TestSetObjective()
        {
            var network = new DistributionNetwork();
            var optimizer = new CoffeeDistributionOptimizer(network);
            optimizer.CreateVariables();
            optimizer.SetObjective();
            Assert.Equal(GRB.MINIMIZE, optimizer.Model.GetObjective().Sense);
        }

        [Fact]
        public void TestAddConstraints()
        {
            var network = new DistributionNetwork();
            var optimizer = new CoffeeDistributionOptimizer(network);
            optimizer.CreateVariables();
            optimizer.SetObjective();
            optimizer.AddConstraints();
            Assert.Equal(12, optimizer.Model.GetConstrs().Length);  // Assuming 2 suppliers, 2 roasteries, and 2 cafes
        }
    }
}