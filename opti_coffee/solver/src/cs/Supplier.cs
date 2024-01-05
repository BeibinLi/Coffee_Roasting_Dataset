using System;
using System.Collections.Generic;

namespace CoffeeDistribution.Entities
{
    public class Supplier
    {
        public string Name { get; private set; }
        public int Capacity { get; private set; }
        public string Location { get; private set; }
        public string Contact { get; private set; }
        public Dictionary<string, int> ShippingCosts { get; private set; }

        public Supplier(string name, int capacity, string location, string contact)
        {
            Name = name;
            Capacity = capacity;
            Location = location;
            Contact = contact;
            ShippingCosts = new Dictionary<string, int>();
        }

        public void SetShippingCost(string roasteryName, int cost)
        {
            ShippingCosts[roasteryName] = cost;
        }

        public int GetShippingCost(string roasteryName)
        {
            return ShippingCosts.TryGetValue(roasteryName, out int cost) ? cost : int.MaxValue;
        }

        public override string ToString()
        {
            return $"Supplier(name={Name}, capacity={Capacity}, location={Location}, contact={Contact})";
        }

        public bool ValidateCapacity(int requestedQuantity)
        {
            return requestedQuantity <= Capacity;
        }

        public void ReduceCapacity(int quantity)
        {
            if (ValidateCapacity(quantity))
            {
                Capacity -= quantity;
            }
            else
            {
                throw new ArgumentException("Requested quantity exceeds capacity");
            }
        }

        public void IncreaseCapacity(int quantity)
        {
            Capacity += quantity;
        }

        public string DisplayInfo()
        {
            var info = $"Name: {Name}\nCapacity: {Capacity}\nLocation: {Location}\nContact: {Contact}\nShipping Costs:\n";
            foreach (var cost in ShippingCosts)
            {
                info += $"  - {cost.Key}: {cost.Value}\n";
            }
            return info;
        }
    }
}