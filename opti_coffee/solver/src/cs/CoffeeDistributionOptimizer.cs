using System;
using System.IO;
using System.Linq;
using Gurobi;
using CoffeeDistribution.Entities;

namespace CoffeeDistribution.Optimizer
{
    public class CoffeeDistributionOptimizer
    {
        public DistributionNetwork Network { get; private set; }
        public GRBModel Model { get; private set; }
        public GRBVar[] Variables { get; private set; }

        public CoffeeDistributionOptimizer(DistributionNetwork network)
        {
            Network = network;
            Model = new GRBModel(new GRBEnv());
        }

        public void CreateVariables()
        {
            int numVariables = Network.Suppliers.Count * Network.Roasteries.Count + Network.Roasteries.Count * Network.Cafes.Count * Network.Cafes[0].CoffeeDemand.Count;
            Variables = new GRBVar[numVariables];

            int index = 0;
            foreach (var supplier in Network.Suppliers)
            {
                foreach (var roastery in Network.Roasteries)
                {
                    Variables[index++] = Model.AddVar(0, GRB.INFINITY, 0, GRB.INTEGER, $"x_{supplier.Name}_{roastery.Name}");
                }
            }

            foreach (var roastery in Network.Roasteries)
            {
                foreach (var cafe in Network.Cafes)
                {
                    foreach (var coffeeType in cafe.CoffeeDemand.Keys)
                    {
                        Variables[index++] = Model.AddVar(0, GRB.INFINITY, 0, GRB.INTEGER, $"y_{roastery.Name}_{cafe.Name}_{coffeeType}");
                    }
                }
            }
        }

        public void SetObjective()
        {
            GRBLinExpr objective = new GRBLinExpr();

            int index = 0;
            foreach (var supplier in Network.Suppliers)
            {
                foreach (var roastery in Network.Roasteries)
                {
                    double cost = Network.GetShippingCostFromSupplierToRoastery(supplier.Name, roastery.Name);
                    objective.AddTerm(cost, Variables[index++]);
                }
            }

            foreach (var roastery in Network.Roasteries)
            {
                foreach (var cafe in Network.Cafes)
                {
                    foreach (var coffeeType in cafe.CoffeeDemand.Keys)
                    {
                        double cost = roastery.GetRoastingCost(coffeeType) + Network.GetShippingCostFromRoasteryToCafe(roastery.Name, cafe.Name);
                        objective.AddTerm(cost, Variables[index++]);
                    }
                }
            }

            Model.SetObjective(objective, GRB.MINIMIZE);
        }

        public void AddConstraints()
        {
            int index = 0;

            // Conservation of flow constraints
            foreach (var roastery in Network.Roasteries)
            {
                GRBLinExpr incomingFlow = new GRBLinExpr();
                GRBLinExpr outgoingFlow = new GRBLinExpr();

                foreach (var supplier in Network.Suppliers)
                {
                    incomingFlow.AddTerm(1, Variables[index++]);
                }

                foreach (var cafe in Network.Cafes)
                {
                    foreach (var coffeeType in cafe.CoffeeDemand.Keys)
                    {
                        outgoingFlow.AddTerm(1, Variables[index++]);
                    }
                }

                Model.AddConstr(incomingFlow == outgoingFlow, $"flow_{roastery.Name}");
            }

            // Supply constraints
            index = 0;
            foreach (var supplier in Network.Suppliers)
            {
                GRBLinExpr outgoingFlow = new GRBLinExpr();

                foreach (var roastery in Network.Roasteries)
                {
                    outgoingFlow.AddTerm(1, Variables[index++]);
                }

                Model.AddConstr(outgoingFlow <= supplier.Capacity, $"supply_{supplier.Name}");
            }

            // Demand constraints
            foreach (var cafe in Network.Cafes)
            {
                foreach (var coffeeType in cafe.CoffeeDemand.Keys)
                {
                    GRBLinExpr incomingFlow = new GRBLinExpr();

                    foreach (var roastery in Network.Roasteries)
                    {
                        incomingFlow.AddTerm(1, Variables[index++]);
                    }

                    Model.AddConstr(incomingFlow >= cafe.GetCoffeeDemand(coffeeType), $"demand_{cafe.Name}_{coffeeType}");
                }
            }
        }

        public void Optimize()
        {
            Model.Optimize();
            if (Model.Status == GRB.Status.OPTIMAL)
            {
                Console.WriteLine($"Optimal cost: {Model.ObjVal}");
            }
            else
            {
                Console.WriteLine("Not solved to optimality. Optimization status: " + Model.Status);
            }
        }

        public void Run()
        {
            CreateVariables();
            SetObjective();
            AddConstraints();
            Optimize();
        }

        public void LogSolution(string outputFile, string header = "")
        {
            Directory.CreateDirectory(Path.GetDirectoryName(outputFile));
            using (StreamWriter writer = new StreamWriter(outputFile))
            {
                writer.WriteLine(header);

                if (Model.Status != GRB.Status.OPTIMAL)
                {
                    writer.WriteLine("No optimal solution found. Cannot log the solution.");
                    return;
                }

                writer.WriteLine("\nOptimal Solution:");
                foreach (var variable in Variables)
                {
                    if (variable.Get(GRB.DoubleAttr.X) != 0)  // Only print non-zero variables
                    {
                        writer.WriteLine($"{variable.VarName}: {variable.Get(GRB.DoubleAttr.X)}");
                    }
                }
            }
        }
    }
}