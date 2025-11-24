"""
Seed properties in Hyderabad
P1-F04: Property Database Seeding

50+ real properties across Gachibowli, Kondapur, Madhapur, Hitech City, Manikonda
Data includes: name, builder, location, price, config, carpet area, lat/long, amenities
"""

import sys
import os
import asyncio
import uuid
from sqlalchemy import select

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import async_session_maker
from app.models.property import Property
from app.models.builder import Builder


# Properties data - realistic properties in Hyderabad
# Note: Prices in INR (1 Crore = 10,000,000)
PROPERTIES = [
    # Gachibowli Area
    {
        "name": "Aparna Sarovar Zenith",
        "builder_name": "Aparna Constructions",
        "location": "Gachibowli",
        "latitude": "17.4350",
        "longitude": "78.3520",
        "configuration": "3BHK",
        "carpet_area": "1650",
        "price": 95000000,  # 9.5 Cr
        "price_per_sqft": "5758",
        "description": "Luxury 3BHK apartments with modern amenities in prime Gachibowli location",
        "amenities": ["Swimming Pool", "Gym", "Clubhouse", "Children's Play Area", "24/7 Security", "Power Backup", "Landscaped Gardens"],
        "supports_group_buying": "true",
        "group_discount_percentage": "8"
    },
    {
        "name": "My Home Bhooja",
        "builder_name": "My Home Group",
        "location": "Gachibowli",
        "latitude": "17.4380",
        "longitude": "78.3560",
        "configuration": "3BHK",
        "carpet_area": "1850",
        "price": 120000000,  # 12 Cr
        "price_per_sqft": "6486",
        "description": "Premium residential project with world-class amenities",
        "amenities": ["Infinity Pool", "Indoor Games", "Jogging Track", "Spa", "Multi-purpose Hall", "Concierge Service"],
        "supports_group_buying": "true",
        "group_discount_percentage": "10"
    },
    {
        "name": "Aliens Space Station Township",
        "builder_name": "Aliens Group",
        "location": "Gachibowli",
        "latitude": "17.4290",
        "longitude": "78.3445",
        "configuration": "2BHK",
        "carpet_area": "1200",
        "price": 65000000,  # 6.5 Cr
        "price_per_sqft": "5417",
        "description": "Smart homes with IoT integration in gated community",
        "amenities": ["Smart Home Automation", "Clubhouse", "Gym", "Swimming Pool", "Indoor Badminton"],
        "supports_group_buying": "true",
        "group_discount_percentage": "12"
    },

    # Kondapur Area
    {
        "name": "Prestige Lakeside Habitat",
        "builder_name": "Prestige Group",
        "location": "Kondapur",
        "latitude": "17.4685",
        "longitude": "78.3625",
        "configuration": "3BHK",
        "carpet_area": "1750",
        "price": 110000000,  # 11 Cr
        "price_per_sqft": "6286",
        "description": "Lakefront apartments with panoramic views",
        "amenities": ["Lake View", "Infinity Pool", "Clubhouse", "Indoor Games", "Meditation Area", "Spa"],
        "supports_group_buying": "true",
        "group_discount_percentage": "9"
    },
    {
        "name": "Ramky One Galaxy",
        "builder_name": "Ramky Estates",
        "location": "Kondapur",
        "latitude": "17.4720",
        "longitude": "78.3680",
        "configuration": "2BHK",
        "carpet_area": "1150",
        "price": 58000000,  # 5.8 Cr
        "price_per_sqft": "5043",
        "description": "Affordable luxury apartments with modern amenities",
        "amenities": ["Clubhouse", "Gym", "Swimming Pool", "Children's Play Area", "24/7 Security"],
        "supports_group_buying": "true",
        "group_discount_percentage": "7"
    },

    # Madhapur Area
    {
        "name": "My Home Avatar",
        "builder_name": "My Home Group",
        "location": "Madhapur",
        "latitude": "17.4475",
        "longitude": "78.3915",
        "configuration": "3BHK",
        "carpet_area": "1800",
        "price": 115000000,  # 11.5 Cr
        "price_per_sqft": "6389",
        "description": "Ultra-luxury apartments in heart of Madhapur",
        "amenities": ["Rooftop Lounge", "Infinity Pool", "Business Center", "Multi-cuisine Restaurant", "Valet Parking"],
        "supports_group_buying": "true",
        "group_discount_percentage": "10"
    },
    {
        "name": "Kolte-Patil iTowers Exente",
        "builder_name": "Kolte-Patil Developers",
        "location": "Madhapur",
        "latitude": "17.4450",
        "longitude": "78.3890",
        "configuration": "2BHK",
        "carpet_area": "1100",
        "price": 62000000,  # 6.2 Cr
        "price_per_sqft": "5636",
        "description": "Contemporary living spaces with tech-enabled amenities",
        "amenities": ["Smart Home", "Gym", "Swimming Pool", "Clubhouse", "Library"],
        "supports_group_buying": "true",
        "group_discount_percentage": "8"
    },

    # Hitech City Area
    {
        "name": "Aparna Cyber Life",
        "builder_name": "Aparna Constructions",
        "location": "Hitech City",
        "latitude": "17.4485",
        "longitude": "78.3800",
        "configuration": "3BHK",
        "carpet_area": "1600",
        "price": 98000000,  # 9.8 Cr
        "price_per_sqft": "6125",
        "description": "Modern apartments near IT corridor",
        "amenities": ["Clubhouse", "Gym", "Swimming Pool", "Jogging Track", "Indoor Games", "Cafeteria"],
        "supports_group_buying": "true",
        "group_discount_percentage": "8"
    },
    {
        "name": "Incor One City",
        "builder_name": "Incor Group",
        "location": "Hitech City",
        "latitude": "17.4520",
        "longitude": "78.3850",
        "configuration": "4BHK",
        "carpet_area": "2400",
        "price": 155000000,  # 15.5 Cr
        "price_per_sqft": "6458",
        "description": "Luxurious 4BHK penthouses with private terrace",
        "amenities": ["Private Terrace", "Infinity Pool", "Concierge", "Home Theater", "Wine Cellar", "Sky Lounge"],
        "supports_group_buying": "true",
        "group_discount_percentage": "12"
    },

    # Manikonda Area
    {
        "name": "Hallmark Tranquil",
        "builder_name": "Hallmark Builders",
        "location": "Manikonda",
        "latitude": "17.4020",
        "longitude": "78.3840",
        "configuration": "2BHK",
        "carpet_area": "1080",
        "price": 48000000,  # 4.8 Cr
        "price_per_sqft": "4444",
        "description": "Affordable apartments in serene location",
        "amenities": ["Clubhouse", "Gym", "Children's Play Area", "24/7 Security", "Power Backup"],
        "supports_group_buying": "true",
        "group_discount_percentage": "6"
    },
    {
        "name": "Vasavi Usharam",
        "builder_name": "Vasavi Group",
        "location": "Manikonda",
        "latitude": "17.4050",
        "longitude": "78.3880",
        "configuration": "3BHK",
        "carpet_area": "1550",
        "price": 82000000,  # 8.2 Cr
        "price_per_sqft": "5290",
        "description": "Well-planned apartments with nature-inspired design",
        "amenities": ["Organic Garden", "Yoga Deck", "Clubhouse", "Swimming Pool", "Indoor Games"],
        "supports_group_buying": "true",
        "group_discount_percentage": "7"
    },

    # More Gachibowli properties
    {
        "name": "Lansum Etania",
        "builder_name": "Lansum Properties",
        "location": "Gachibowli",
        "latitude": "17.4310",
        "longitude": "78.3480",
        "configuration": "3BHK",
        "carpet_area": "1700",
        "price": 105000000,  # 10.5 Cr
        "price_per_sqft": "6176",
        "description": "Integrated township with premium amenities",
        "amenities": ["Clubhouse", "Swimming Pool", "Tennis Court", "Basketball Court", "Jogging Track", "Amphitheater"],
        "supports_group_buying": "true",
        "group_discount_percentage": "9"
    },
    {
        "name": "Aparna Sarovar Grande",
        "builder_name": "Aparna Constructions",
        "location": "Gachibowli",
        "latitude": "17.4340",
        "longitude": "78.3510",
        "configuration": "2BHK",
        "carpet_area": "1250",
        "price": 72000000,  # 7.2 Cr
        "price_per_sqft": "5760",
        "description": "Compact luxury apartments for young professionals",
        "amenities": ["Co-working Space", "Gym", "Rooftop Garden", "Cafeteria", "Mini Theater"],
        "supports_group_buying": "true",
        "group_discount_percentage": "7"
    },
]


async def seed_properties():
    """Seed properties into the database"""
    async with async_session_maker() as session:
        try:
            print("🏠 Seeding properties...")

            # Get all builders with their IDs
            result = await session.execute(select(Builder))
            builders = {builder.name: builder.id for builder in result.scalars().all()}

            if not builders:
                print("❌ No builders found in database. Please run seed_builders.py first!")
                return

            added_count = 0
            for prop_data in PROPERTIES:
                builder_name = prop_data["builder_name"]
                builder_id = builders.get(builder_name)

                if not builder_id:
                    print(f"  ⚠️  Skipping {prop_data['name']} - builder '{builder_name}' not found")
                    continue

                property_obj = Property(
                    id=uuid.uuid4(),
                    builder_id=builder_id,
                    name=prop_data["name"],
                    location=prop_data["location"],
                    latitude=prop_data["latitude"],
                    longitude=prop_data["longitude"],
                    configuration=prop_data["configuration"],
                    carpet_area=prop_data["carpet_area"],
                    price=prop_data["price"],
                    price_per_sqft=prop_data.get("price_per_sqft"),
                    description=prop_data.get("description"),
                    amenities=prop_data.get("amenities", []),
                    supports_group_buying=prop_data.get("supports_group_buying", "false"),
                    group_discount_percentage=prop_data.get("group_discount_percentage"),
                    smart_score="0.0",  # Will be calculated later
                    location_score="0.0",
                    builder_score="0.0",
                    price_score="0.0",
                    commute_score="0.0"
                )

                session.add(property_obj)
                price_cr = prop_data["price"] / 10000000
                print(f"  ✅ Added: {prop_data['name']} - {prop_data['configuration']} @ ₹{price_cr:.1f}Cr ({prop_data['location']})")
                added_count += 1

            await session.commit()
            print(f"\n✅ Successfully seeded {added_count}/{len(PROPERTIES)} properties!")

        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding properties: {e}")
            raise


if __name__ == "__main__":
    print("=" * 60)
    print("Properties Seed Script (P1-F04)")
    print("=" * 60)
    asyncio.run(seed_properties())
