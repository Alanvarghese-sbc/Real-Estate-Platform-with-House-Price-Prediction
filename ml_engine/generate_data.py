import pandas as pd
import numpy as np
import random

def generate_house_prices_data(num_samples=1000):
    """Generate realistic house price dataset for Kerala"""
    districts = [
        "Ernakulam", "Trivandrum", "Kottayam", "Thrissur", "Kozhikode",
        "Kollam", "Alappuzha", "Palakkad", "Malappuram", "Kannur",
        "Wayanad", "Idukki", "Pathanamthitta", "Kasargod"
    ]
    
    locations = {
        "Ernakulam": ["Kochi", "Edappally", "Kakkanad", "Palarivattom", "Aluva"],
        "Trivandrum": ["Kazhakkoottam", "Pattom", "Kowdiar", "Technopark", "Vellayambalam"],
        "Kottayam": ["Kanjikuzhy", "Baker Junction", "Nagampadam", "Ettumanoor", "Pala"],
        "Thrissur": ["Swaraj Round", "Ayyanthole", "Poonkunnam", "Olarikkara", "Viyyur"],
        "Kozhikode": ["Mavoor Road", "Nadakkavu", "West Hill", "Beach Road", "Mananchira"]
    }
    
    default_locations = ["Town Center", "Suburbs", "Rural Area", "Near Highway", "Residential Area"]

    data = []
    
    for i in range(num_samples):
        district = random.choice(districts)
        
        if district in locations:
            location = random.choice(locations[district])
        else:
            location = random.choice(default_locations)
            
        # Realistic features
        area = random.randint(500, 5000)  # sq ft
        bedrooms = random.randint(1, 6)
        
        # Base price per sq ft varies by district
        base_price_sqft = 3000
        if district == "Ernakulam": 
            base_price_sqft = 5000
        elif district == "Trivandrum": 
            base_price_sqft = 4500
        elif district == "Kozhikode": 
            base_price_sqft = 4000
        elif district == "Kottayam": 
            base_price_sqft = 3500
        elif district == "Thrissur": 
            base_price_sqft = 3800
        
        # Adjust base price slightly randomly
        base_price_sqft += random.randint(-500, 500)
        
        # Calculate price
        base_price = (area * base_price_sqft)
        
        # Add value for bedrooms
        bedroom_premium = (bedrooms - 1) * random.randint(200000, 500000)
        
        price = base_price + bedroom_premium
        
        # Add some random noise
        price += random.randint(-200000, 200000)
        
        # Ensure positive
        price = max(1000000, price)
        
        data.append({
            "District": district,
            "Location": location,
            "Area": area,
            "Bedrooms": bedrooms,
            "Price": int(price)
        })
        
    df = pd.DataFrame(data)
    df.to_csv("house_prices.csv", index=False)
    print(f"CSV generated successfully with {len(df)} records.")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Price range: Rs.{df['Price'].min():,} - Rs.{df['Price'].max():,}")

if __name__ == "__main__":
    generate_house_prices_data()
