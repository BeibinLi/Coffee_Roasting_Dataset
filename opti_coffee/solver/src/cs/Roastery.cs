using System;
using System.Collections.Generic;

namespace CoffeeDistribution.Entities
{
    public class Roastery
    {
        public string Name { get; private set; }
        public string Location { get; private set; }
        public string Contact { get; private set; }
        public Dictionary<string, (int Cost, string Constraints)> RoastingCosts { get; private set; }
        public Dictionary<string, int> ShippingCosts { get; private set; }

        public Roastery(string name, string location, string contact)
        {
            Name = name;
            Location = location;
            Contact = contact;
            RoastingCosts = new Dictionary<string, (int Cost, string Constraints)>();
            ShippingCosts = new Dictionary<string, int>();
        }

        public void SetRoastingCost(string coffeeType, int cost, string constraints = null)
        {
            RoastingCosts[coffeeType] = (cost, constraints);
        }

        public void SetShippingCost(string cafeName, int cost)
        {
            ShippingCosts[cafeName] = cost;
        }

        public int GetShippingCost(string cafeName)
        {
            return ShippingCosts.TryGetValue(cafeName, out int cost) ? cost : int.MaxValue;
        }

        public int GetRoastingCost(string coffeeType)
        {
            return RoastingCosts.TryGetValue(coffeeType, out (int Cost, string Constraints) details) ? details.Cost : int.MaxValue;
        }

        public string GetRoastingConstraints(string coffeeType)
        {
            return RoastingCosts.TryGetValue(coffeeType, out (int Cost, string Constraints) details) ? details.Constraints : null;
        }

        public string DisplayInfo()
        {
            var info = $"Name: {Name}\nLocation: {Location}\nContact: {Contact}\nRoasting Costs:\n";
            foreach (var cost in RoastingCosts)
            {
                info += $"  - {cost.Key}: {cost.Value.Cost} (Constraints: {cost.Value.Constraints})\n";
            }
            info += "Shipping Costs:\n";
            foreach (var cost in ShippingCosts)
            {
                info += $"  - {cost.Key}: {cost.Value}\n";
            }
            return info;
        }

        public override string ToString()
        {
            return $"Roastery(name={Name}, location={Location}, contact={Contact})";
        }

        public bool ValidateRoastingConstraints(string coffeeType, string constraints)
        {
            string requiredConstraints = GetRoastingConstraints(coffeeType);
            return requiredConstraints == null || requiredConstraints == constraints;
        }
    }
}