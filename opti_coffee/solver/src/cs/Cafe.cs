using System;
using System.Collections.Generic;

namespace CoffeeDistribution.Entities
{
    public class Cafe
    {
        public string Name { get; private set; }
        public string Location { get; private set; }
        public string Contact { get; private set; }
        public Dictionary<string, int> CoffeeDemand { get; private set; }

        public Cafe(string name, string location, string contact)
        {
            Name = name;
            Location = location;
            Contact = contact;
            CoffeeDemand = new Dictionary<string, int>();
        }

        public void SetCoffeeDemand(string coffeeType, int quantity)
        {
            CoffeeDemand[coffeeType] = quantity;
        }

        public int GetCoffeeDemand(string coffeeType)
        {
            return CoffeeDemand.TryGetValue(coffeeType, out int quantity) ? quantity : 0;
        }

        public string DisplayInfo()
        {
            var info = $"Name: {Name}\nLocation: {Location}\nContact: {Contact}\nCoffee Demand:\n";
            foreach (var demand in CoffeeDemand)
            {
                info += $"  - {demand.Key}: {demand.Value}\n";
            }
            return info;
        }

        public override string ToString()
        {
            return $"Cafe(name={Name}, location={Location}, contact={Contact})";
        }

        public void FulfillDemand(string coffeeType, int quantity)
        {
            int currentDemand = GetCoffeeDemand(coffeeType);
            if (quantity > currentDemand)
            {
                throw new ArgumentException("Fulfilled quantity exceeds demand");
            }
            CoffeeDemand[coffeeType] = currentDemand - quantity;
        }
    }
}