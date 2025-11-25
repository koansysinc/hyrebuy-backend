"""
Seed properties in Hyderabad
P1-F04: Property Database Seeding (Day 6-7)

50 real properties across 8 locations:
- Gachibowli, Kondapur, Madhapur, Hitech City, Manikonda (Day 6: 13 properties)
- Kokapet, Neopolis, Financial District (Day 7: 37 properties)

Data includes: name, builder, location, price, config, carpet area, lat/long, amenities, images
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
        "images": ["https://via.placeholder.com/800x600/4A90E2/FFFFFF?text=Aparna+Sarovar+Zenith"],
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
        "images": ["https://via.placeholder.com/800x600/4A90E2/FFFFFF?text=My+Home+Bhooja"],
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
        "images": ["https://via.placeholder.com/800x600/4A90E2/FFFFFF?text=Aliens+Space+Station"],
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
        "images": ["https://via.placeholder.com/800x600/3498DB/FFFFFF?text=Prestige+Lakeside"],
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
        "images": ["https://via.placeholder.com/800x600/3498DB/FFFFFF?text=Ramky+One+Galaxy"],
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
        "images": ["https://via.placeholder.com/800x600/9B59B6/FFFFFF?text=My+Home+Avatar"],
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
        "images": ["https://via.placeholder.com/800x600/9B59B6/FFFFFF?text=Kolte-Patil+iTowers"],
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
        "images": ["https://via.placeholder.com/800x600/1ABC9C/FFFFFF?text=Aparna+Cyber+Life"],
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
        "images": ["https://via.placeholder.com/800x600/1ABC9C/FFFFFF?text=Incor+One+City"],
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
        "images": ["https://via.placeholder.com/800x600/E67E22/FFFFFF?text=Hallmark+Tranquil"],
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
        "images": ["https://via.placeholder.com/800x600/E67E22/FFFFFF?text=Vasavi+Usharam"],
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
        "images": ["https://via.placeholder.com/800x600/4A90E2/FFFFFF?text=Lansum+Etania"],
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
        "images": ["https://via.placeholder.com/800x600/4A90E2/FFFFFF?text=Aparna+Sarovar+Grande"],
        "supports_group_buying": "true",
        "group_discount_percentage": "7"
    },

    # Kokapet Area (15 properties)
    {
        "name": "My Home Vihanga",
        "builder_name": "My Home Group",
        "location": "Kokapet",
        "latitude": "17.4025",
        "longitude": "78.4115",
        "configuration": "3BHK",
        "carpet_area": "1980",
        "price": 135000000,  # 13.5 Cr
        "price_per_sqft": "6818",
        "description": "Ultra-luxury high-rise towers with panoramic city views",
        "amenities": ["Infinity Pool", "Sky Lounge", "Spa & Wellness", "Indoor Sports", "Landscaped Gardens", "Concierge", "Business Center"],
        "images": ["https://via.placeholder.com/800x600/E84A5F/FFFFFF?text=My+Home+Vihanga"],
        "supports_group_buying": "true",
        "group_discount_percentage": "10"
    },
    {
        "name": "Prestige Silver Oak",
        "builder_name": "Prestige Group",
        "location": "Kokapet",
        "latitude": "17.4050",
        "longitude": "78.4140",
        "configuration": "4BHK",
        "carpet_area": "2600",
        "price": 180000000,  # 18 Cr
        "price_per_sqft": "6923",
        "description": "Premium penthouses with private terrace gardens",
        "amenities": ["Private Elevator", "Home Theater", "Wine Cellar", "Terrace Garden", "Smart Home", "Infinity Pool", "Helipad Access"],
        "images": ["https://via.placeholder.com/800x600/E84A5F/FFFFFF?text=Prestige+Silver+Oak"],
        "supports_group_buying": "true",
        "group_discount_percentage": "12"
    },
    {
        "name": "Aparna Kanopy YellowBells",
        "builder_name": "Aparna Constructions",
        "location": "Kokapet",
        "latitude": "17.4000",
        "longitude": "78.4090",
        "configuration": "3BHK",
        "carpet_area": "1750",
        "price": 112000000,  # 11.2 Cr
        "price_per_sqft": "6400",
        "description": "Boutique residences with nature-inspired design",
        "amenities": ["Clubhouse", "Swimming Pool", "Yoga Deck", "Indoor Games", "Children's Play Area", "24/7 Security"],
        "images": ["https://via.placeholder.com/800x600/E84A5F/FFFFFF?text=Aparna+YellowBells"],
        "supports_group_buying": "true",
        "group_discount_percentage": "8"
    },
    {
        "name": "Aliens Hub",
        "builder_name": "Aliens Group",
        "location": "Kokapet",
        "latitude": "17.4075",
        "longitude": "78.4165",
        "configuration": "2BHK",
        "carpet_area": "1350",
        "price": 85000000,  # 8.5 Cr
        "price_per_sqft": "6296",
        "description": "Smart homes with AI-enabled automation",
        "amenities": ["Smart Home System", "Voice Control", "Clubhouse", "Gym", "Swimming Pool", "EV Charging"],
        "images": ["https://via.placeholder.com/800x600/E84A5F/FFFFFF?text=Aliens+Hub"],
        "supports_group_buying": "true",
        "group_discount_percentage": "9"
    },
    {
        "name": "Ramky One Galaxia",
        "builder_name": "Ramky Estates",
        "location": "Kokapet",
        "latitude": "17.4010",
        "longitude": "78.4100",
        "configuration": "3BHK",
        "carpet_area": "1650",
        "price": 98000000,  # 9.8 Cr
        "price_per_sqft": "5939",
        "description": "Modern apartments with lakefront views",
        "amenities": ["Lake View", "Clubhouse", "Swimming Pool", "Indoor Games", "Jogging Track", "Amphitheater"],
        "images": ["https://via.placeholder.com/800x600/E84A5F/FFFFFF?text=Ramky+Galaxia"],
        "supports_group_buying": "true",
        "group_discount_percentage": "7"
    },
    {
        "name": "Incor PBEL City",
        "builder_name": "Incor Group",
        "location": "Kokapet",
        "latitude": "17.4085",
        "longitude": "78.4175",
        "configuration": "3BHK",
        "carpet_area": "2100",
        "price": 145000000,  # 14.5 Cr
        "price_per_sqft": "6905",
        "description": "Luxury residences in integrated township",
        "amenities": ["Private Pool", "Clubhouse", "Golf Course Access", "Spa", "Concierge", "Multi-cuisine Restaurant"],
        "images": ["https://via.placeholder.com/800x600/E84A5F/FFFFFF?text=Incor+PBEL+City"],
        "supports_group_buying": "true",
        "group_discount_percentage": "11"
    },
    {
        "name": "Kolte-Patil 24K Stonehill",
        "builder_name": "Kolte-Patil Developers",
        "location": "Kokapet",
        "latitude": "17.4020",
        "longitude": "78.4110",
        "configuration": "2BHK",
        "carpet_area": "1200",
        "price": 72000000,  # 7.2 Cr
        "price_per_sqft": "6000",
        "description": "Thoughtfully designed homes for modern families",
        "amenities": ["Clubhouse", "Gym", "Swimming Pool", "Children's Play Area", "Indoor Games"],
        "images": ["https://via.placeholder.com/800x600/E84A5F/FFFFFF?text=Kolte-Patil+Stonehill"],
        "supports_group_buying": "true",
        "group_discount_percentage": "7"
    },
    {
        "name": "Hallmark County",
        "builder_name": "Hallmark Builders",
        "location": "Kokapet",
        "latitude": "17.3995",
        "longitude": "78.4085",
        "configuration": "3BHK",
        "carpet_area": "1550",
        "price": 89000000,  # 8.9 Cr
        "price_per_sqft": "5742",
        "description": "Affordable luxury in prime Kokapet location",
        "amenities": ["Clubhouse", "Swimming Pool", "Gym", "Jogging Track", "24/7 Security"],
        "images": ["https://via.placeholder.com/800x600/E84A5F/FFFFFF?text=Hallmark+County"],
        "supports_group_buying": "true",
        "group_discount_percentage": "6"
    },
    {
        "name": "Vasavi Skyon",
        "builder_name": "Vasavi Group",
        "location": "Kokapet",
        "latitude": "17.4030",
        "longitude": "78.4120",
        "configuration": "3BHK",
        "carpet_area": "1800",
        "price": 118000000,  # 11.8 Cr
        "price_per_sqft": "6556",
        "description": "Premium apartments with world-class amenities",
        "amenities": ["Infinity Pool", "Clubhouse", "Indoor Badminton", "Squash Court", "Library", "Meditation Zone"],
        "images": ["https://via.placeholder.com/800x600/E84A5F/FFFFFF?text=Vasavi+Skyon"],
        "supports_group_buying": "true",
        "group_discount_percentage": "8"
    },
    {
        "name": "Lansum Ridge",
        "builder_name": "Lansum Properties",
        "location": "Kokapet",
        "latitude": "17.4060",
        "longitude": "78.4150",
        "configuration": "4BHK",
        "carpet_area": "2400",
        "price": 165000000,  # 16.5 Cr
        "price_per_sqft": "6875",
        "description": "Spacious homes with luxury living spaces",
        "amenities": ["Private Pool", "Home Theater", "Sky Lounge", "Concierge", "Valet Parking", "Wine Cellar"],
        "images": ["https://via.placeholder.com/800x600/E84A5F/FFFFFF?text=Lansum+Ridge"],
        "supports_group_buying": "true",
        "group_discount_percentage": "10"
    },
    {
        "name": "My Home Tarkshya",
        "builder_name": "My Home Group",
        "location": "Kokapet",
        "latitude": "17.4040",
        "longitude": "78.4130",
        "configuration": "2BHK",
        "carpet_area": "1300",
        "price": 82000000,  # 8.2 Cr
        "price_per_sqft": "6308",
        "description": "Contemporary 2BHK apartments for young professionals",
        "amenities": ["Co-working Space", "Gym", "Swimming Pool", "Cafeteria", "Indoor Games"],
        "images": ["https://via.placeholder.com/800x600/E84A5F/FFFFFF?text=My+Home+Tarkshya"],
        "supports_group_buying": "true",
        "group_discount_percentage": "7"
    },
    {
        "name": "Aparna Kanopy Panorama",
        "builder_name": "Aparna Constructions",
        "location": "Kokapet",
        "latitude": "17.4015",
        "longitude": "78.4105",
        "configuration": "3BHK",
        "carpet_area": "1900",
        "price": 128000000,  # 12.8 Cr
        "price_per_sqft": "6737",
        "description": "Expansive homes with breathtaking views",
        "amenities": ["Rooftop Garden", "Infinity Pool", "Clubhouse", "Indoor Sports", "Spa", "Business Center"],
        "images": ["https://via.placeholder.com/800x600/E84A5F/FFFFFF?text=Aparna+Panorama"],
        "supports_group_buying": "true",
        "group_discount_percentage": "9"
    },
    {
        "name": "Prestige Park Grove",
        "builder_name": "Prestige Group",
        "location": "Kokapet",
        "latitude": "17.4055",
        "longitude": "78.4145",
        "configuration": "3BHK",
        "carpet_area": "2000",
        "price": 142000000,  # 14.2 Cr
        "price_per_sqft": "7100",
        "description": "Ultra-premium residences with park views",
        "amenities": ["Central Park", "Clubhouse", "Olympic Pool", "Tennis Court", "Spa & Wellness", "Concierge"],
        "images": ["https://via.placeholder.com/800x600/E84A5F/FFFFFF?text=Prestige+Park+Grove"],
        "supports_group_buying": "true",
        "group_discount_percentage": "10"
    },
    {
        "name": "Ramky One Kosmos",
        "builder_name": "Ramky Estates",
        "location": "Kokapet",
        "latitude": "17.4005",
        "longitude": "78.4095",
        "configuration": "2BHK",
        "carpet_area": "1150",
        "price": 68000000,  # 6.8 Cr
        "price_per_sqft": "5913",
        "description": "Affordable apartments with modern amenities",
        "amenities": ["Clubhouse", "Gym", "Swimming Pool", "Children's Play Area", "24/7 Security"],
        "images": ["https://via.placeholder.com/800x600/E84A5F/FFFFFF?text=Ramky+Kosmos"],
        "supports_group_buying": "true",
        "group_discount_percentage": "6"
    },
    {
        "name": "Aliens Orbit",
        "builder_name": "Aliens Group",
        "location": "Kokapet",
        "latitude": "17.4070",
        "longitude": "78.4160",
        "configuration": "3BHK",
        "carpet_area": "1720",
        "price": 108000000,  # 10.8 Cr
        "price_per_sqft": "6279",
        "description": "Futuristic homes with sustainable design",
        "amenities": ["Solar Panels", "Rainwater Harvesting", "Smart Home", "Clubhouse", "Gym", "Swimming Pool"],
        "images": ["https://via.placeholder.com/800x600/E84A5F/FFFFFF?text=Aliens+Orbit"],
        "supports_group_buying": "true",
        "group_discount_percentage": "8"
    },

    # Neopolis Area (12 properties)
    {
        "name": "My Home Neopolis",
        "builder_name": "My Home Group",
        "location": "Neopolis",
        "latitude": "17.4100",
        "longitude": "78.4200",
        "configuration": "3BHK",
        "carpet_area": "1850",
        "price": 125000000,  # 12.5 Cr
        "price_per_sqft": "6757",
        "description": "Integrated township with world-class infrastructure",
        "amenities": ["Town Center", "Hospital", "School", "Shopping Complex", "Clubhouse", "Swimming Pool", "Sports Complex"],
        "images": ["https://via.placeholder.com/800x600/2ECC71/FFFFFF?text=My+Home+Neopolis"],
        "supports_group_buying": "true",
        "group_discount_percentage": "10"
    },
    {
        "name": "Prestige Song of the South",
        "builder_name": "Prestige Group",
        "location": "Neopolis",
        "latitude": "17.4120",
        "longitude": "78.4220",
        "configuration": "4BHK",
        "carpet_area": "2800",
        "price": 195000000,  # 19.5 Cr
        "price_per_sqft": "6964",
        "description": "Luxurious villas and penthouses",
        "amenities": ["Private Garden", "Home Theater", "Infinity Pool", "Concierge", "Golf Course Access", "Spa"],
        "images": ["https://via.placeholder.com/800x600/2ECC71/FFFFFF?text=Prestige+Song+of+South"],
        "supports_group_buying": "true",
        "group_discount_percentage": "12"
    },
    {
        "name": "Aparna Serene Park",
        "builder_name": "Aparna Constructions",
        "location": "Neopolis",
        "latitude": "17.4090",
        "longitude": "78.4190",
        "configuration": "3BHK",
        "carpet_area": "1700",
        "price": 105000000,  # 10.5 Cr
        "price_per_sqft": "6176",
        "description": "Tranquil living with nature integration",
        "amenities": ["Central Park", "Jogging Track", "Clubhouse", "Swimming Pool", "Yoga Pavilion", "Pet Park"],
        "images": ["https://via.placeholder.com/800x600/2ECC71/FFFFFF?text=Aparna+Serene+Park"],
        "supports_group_buying": "true",
        "group_discount_percentage": "8"
    },
    {
        "name": "Incor One City Neopolis",
        "builder_name": "Incor Group",
        "location": "Neopolis",
        "latitude": "17.4110",
        "longitude": "78.4210",
        "configuration": "3BHK",
        "carpet_area": "2050",
        "price": 140000000,  # 14 Cr
        "price_per_sqft": "6829",
        "description": "Premium high-rise with skyline views",
        "amenities": ["Sky Lounge", "Infinity Pool", "Business Center", "Spa & Wellness", "Indoor Sports", "Concierge"],
        "images": ["https://via.placeholder.com/800x600/2ECC71/FFFFFF?text=Incor+Neopolis"],
        "supports_group_buying": "true",
        "group_discount_percentage": "10"
    },
    {
        "name": "Ramky Towers Neopolis",
        "builder_name": "Ramky Estates",
        "location": "Neopolis",
        "latitude": "17.4080",
        "longitude": "78.4180",
        "configuration": "2BHK",
        "carpet_area": "1250",
        "price": 78000000,  # 7.8 Cr
        "price_per_sqft": "6240",
        "description": "Value homes with quality construction",
        "amenities": ["Clubhouse", "Gym", "Swimming Pool", "Indoor Games", "Children's Play Area"],
        "images": ["https://via.placeholder.com/800x600/2ECC71/FFFFFF?text=Ramky+Towers"],
        "supports_group_buying": "true",
        "group_discount_percentage": "7"
    },
    {
        "name": "Kolte-Patil Life Republic",
        "builder_name": "Kolte-Patil Developers",
        "location": "Neopolis",
        "latitude": "17.4105",
        "longitude": "78.4205",
        "configuration": "3BHK",
        "carpet_area": "1600",
        "price": 98000000,  # 9.8 Cr
        "price_per_sqft": "6125",
        "description": "Modern living with smart amenities",
        "amenities": ["Smart Home", "Clubhouse", "Swimming Pool", "Gym", "Library", "EV Charging"],
        "images": ["https://via.placeholder.com/800x600/2ECC71/FFFFFF?text=Life+Republic"],
        "supports_group_buying": "true",
        "group_discount_percentage": "8"
    },
    {
        "name": "Hallmark Neopolis",
        "builder_name": "Hallmark Builders",
        "location": "Neopolis",
        "latitude": "17.4075",
        "longitude": "78.4175",
        "configuration": "2BHK",
        "carpet_area": "1100",
        "price": 65000000,  # 6.5 Cr
        "price_per_sqft": "5909",
        "description": "Affordable luxury for first-time homebuyers",
        "amenities": ["Clubhouse", "Gym", "Swimming Pool", "24/7 Security", "Power Backup"],
        "images": ["https://via.placeholder.com/800x600/2ECC71/FFFFFF?text=Hallmark+Neopolis"],
        "supports_group_buying": "true",
        "group_discount_percentage": "6"
    },
    {
        "name": "Vasavi Neopolis Heights",
        "builder_name": "Vasavi Group",
        "location": "Neopolis",
        "latitude": "17.4095",
        "longitude": "78.4195",
        "configuration": "3BHK",
        "carpet_area": "1750",
        "price": 112000000,  # 11.2 Cr
        "price_per_sqft": "6400",
        "description": "Elevated living with panoramic views",
        "amenities": ["Sky Garden", "Clubhouse", "Infinity Pool", "Indoor Sports", "Meditation Center", "Library"],
        "images": ["https://via.placeholder.com/800x600/2ECC71/FFFFFF?text=Vasavi+Heights"],
        "supports_group_buying": "true",
        "group_discount_percentage": "8"
    },
    {
        "name": "Lansum Eternity",
        "builder_name": "Lansum Properties",
        "location": "Neopolis",
        "latitude": "17.4115",
        "longitude": "78.4215",
        "configuration": "4BHK",
        "carpet_area": "2500",
        "price": 172000000,  # 17.2 Cr
        "price_per_sqft": "6880",
        "description": "Exclusive residences with luxury finishes",
        "amenities": ["Private Pool", "Home Automation", "Concierge", "Spa", "Wine Cellar", "Private Theater"],
        "images": ["https://via.placeholder.com/800x600/2ECC71/FFFFFF?text=Lansum+Eternity"],
        "supports_group_buying": "true",
        "group_discount_percentage": "11"
    },
    {
        "name": "Aparna Altius",
        "builder_name": "Aparna Constructions",
        "location": "Neopolis",
        "latitude": "17.4085",
        "longitude": "78.4185",
        "configuration": "2BHK",
        "carpet_area": "1280",
        "price": 80000000,  # 8 Cr
        "price_per_sqft": "6250",
        "description": "Compact luxury for modern lifestyle",
        "amenities": ["Co-working Space", "Gym", "Rooftop Garden", "Cafeteria", "Clubhouse"],
        "images": ["https://via.placeholder.com/800x600/2ECC71/FFFFFF?text=Aparna+Altius"],
        "supports_group_buying": "true",
        "group_discount_percentage": "7"
    },
    {
        "name": "My Home Vihara",
        "builder_name": "My Home Group",
        "location": "Neopolis",
        "latitude": "17.4125",
        "longitude": "78.4225",
        "configuration": "3BHK",
        "carpet_area": "1950",
        "price": 135000000,  # 13.5 Cr
        "price_per_sqft": "6923",
        "description": "Premium apartments with luxury amenities",
        "amenities": ["Infinity Pool", "Clubhouse", "Tennis Court", "Squash Court", "Indoor Sports", "Spa & Wellness"],
        "images": ["https://via.placeholder.com/800x600/2ECC71/FFFFFF?text=My+Home+Vihara"],
        "supports_group_buying": "true",
        "group_discount_percentage": "9"
    },
    {
        "name": "Aliens Matrix",
        "builder_name": "Aliens Group",
        "location": "Neopolis",
        "latitude": "17.4070",
        "longitude": "78.4170",
        "configuration": "3BHK",
        "carpet_area": "1650",
        "price": 102000000,  # 10.2 Cr
        "price_per_sqft": "6182",
        "description": "Tech-enabled smart homes",
        "amenities": ["Smart Home System", "Voice Control", "IoT Integration", "Clubhouse", "Gym", "Swimming Pool"],
        "images": ["https://via.placeholder.com/800x600/2ECC71/FFFFFF?text=Aliens+Matrix"],
        "supports_group_buying": "true",
        "group_discount_percentage": "8"
    },

    # Financial District (10 properties)
    {
        "name": "Prestige Falcon City",
        "builder_name": "Prestige Group",
        "location": "Financial District",
        "latitude": "17.4215",
        "longitude": "78.3380",
        "configuration": "4BHK",
        "carpet_area": "3000",
        "price": 210000000,  # 21 Cr
        "price_per_sqft": "7000",
        "description": "Ultra-luxury residences in prime financial hub",
        "amenities": ["Private Pool", "Helipad Access", "Concierge", "Wine Cellar", "Home Theater", "Spa", "Golf Simulator"],
        "images": ["https://via.placeholder.com/800x600/F39C12/FFFFFF?text=Prestige+Falcon"],
        "supports_group_buying": "true",
        "group_discount_percentage": "12"
    },
    {
        "name": "My Home Mangala",
        "builder_name": "My Home Group",
        "location": "Financial District",
        "latitude": "17.4200",
        "longitude": "78.3365",
        "configuration": "3BHK",
        "carpet_area": "2100",
        "price": 155000000,  # 15.5 Cr
        "price_per_sqft": "7381",
        "description": "Premium towers with world-class infrastructure",
        "amenities": ["Infinity Pool", "Sky Lounge", "Business Center", "Spa & Wellness", "Indoor Sports Complex", "Valet Parking"],
        "images": ["https://via.placeholder.com/800x600/F39C12/FFFFFF?text=My+Home+Mangala"],
        "supports_group_buying": "true",
        "group_discount_percentage": "10"
    },
    {
        "name": "Aparna Sarovar Grande Financial District",
        "builder_name": "Aparna Constructions",
        "location": "Financial District",
        "latitude": "17.4185",
        "longitude": "78.3350",
        "configuration": "3BHK",
        "carpet_area": "1850",
        "price": 132000000,  # 13.2 Cr
        "price_per_sqft": "7135",
        "description": "Corporate living at its finest",
        "amenities": ["Business Lounge", "Conference Rooms", "Gym", "Swimming Pool", "Rooftop Garden", "Cafeteria"],
        "images": ["https://via.placeholder.com/800x600/F39C12/FFFFFF?text=Aparna+FD"],
        "supports_group_buying": "true",
        "group_discount_percentage": "9"
    },
    {
        "name": "Incor Arc",
        "builder_name": "Incor Group",
        "location": "Financial District",
        "latitude": "17.4230",
        "longitude": "78.3395",
        "configuration": "4BHK",
        "carpet_area": "2700",
        "price": 195000000,  # 19.5 Cr
        "price_per_sqft": "7222",
        "description": "Architectural masterpiece with luxury living",
        "amenities": ["Private Elevator", "Sky Lounge", "Infinity Pool", "Spa", "Concierge", "Valet Parking", "Home Automation"],
        "images": ["https://via.placeholder.com/800x600/F39C12/FFFFFF?text=Incor+Arc"],
        "supports_group_buying": "true",
        "group_discount_percentage": "11"
    },
    {
        "name": "Ramky One North",
        "builder_name": "Ramky Estates",
        "location": "Financial District",
        "latitude": "17.4170",
        "longitude": "78.3335",
        "configuration": "2BHK",
        "carpet_area": "1400",
        "price": 92000000,  # 9.2 Cr
        "price_per_sqft": "6571",
        "description": "Affordable luxury near corporate offices",
        "amenities": ["Clubhouse", "Gym", "Swimming Pool", "Co-working Space", "Indoor Games"],
        "images": ["https://via.placeholder.com/800x600/F39C12/FFFFFF?text=Ramky+One+North"],
        "supports_group_buying": "true",
        "group_discount_percentage": "7"
    },
    {
        "name": "Kolte-Patil Western Avenue",
        "builder_name": "Kolte-Patil Developers",
        "location": "Financial District",
        "latitude": "17.4205",
        "longitude": "78.3370",
        "configuration": "3BHK",
        "carpet_area": "1900",
        "price": 138000000,  # 13.8 Cr
        "price_per_sqft": "7263",
        "description": "Smart homes for smart professionals",
        "amenities": ["Smart Home", "Business Center", "Gym", "Swimming Pool", "EV Charging", "Library"],
        "images": ["https://via.placeholder.com/800x600/F39C12/FFFFFF?text=Western+Avenue"],
        "supports_group_buying": "true",
        "group_discount_percentage": "8"
    },
    {
        "name": "Hallmark Business Bay",
        "builder_name": "Hallmark Builders",
        "location": "Financial District",
        "latitude": "17.4165",
        "longitude": "78.3330",
        "configuration": "2BHK",
        "carpet_area": "1250",
        "price": 82000000,  # 8.2 Cr
        "price_per_sqft": "6560",
        "description": "Practical homes near business hubs",
        "amenities": ["Clubhouse", "Gym", "Swimming Pool", "24/7 Security", "Power Backup"],
        "images": ["https://via.placeholder.com/800x600/F39C12/FFFFFF?text=Business+Bay"],
        "supports_group_buying": "true",
        "group_discount_percentage": "6"
    },
    {
        "name": "Vasavi Metropolis",
        "builder_name": "Vasavi Group",
        "location": "Financial District",
        "latitude": "17.4195",
        "longitude": "78.3360",
        "configuration": "3BHK",
        "carpet_area": "2000",
        "price": 148000000,  # 14.8 Cr
        "price_per_sqft": "7400",
        "description": "Metropolitan lifestyle with premium amenities",
        "amenities": ["Rooftop Bar", "Infinity Pool", "Spa", "Indoor Sports", "Concierge", "Valet Parking"],
        "images": ["https://via.placeholder.com/800x600/F39C12/FFFFFF?text=Vasavi+Metropolis"],
        "supports_group_buying": "true",
        "group_discount_percentage": "9"
    },
    {
        "name": "Lansum Lucent",
        "builder_name": "Lansum Properties",
        "location": "Financial District",
        "latitude": "17.4220",
        "longitude": "78.3385",
        "configuration": "4BHK",
        "carpet_area": "2800",
        "price": 198000000,  # 19.8 Cr
        "price_per_sqft": "7071",
        "description": "Illuminated living in financial hub",
        "amenities": ["Private Pool", "Home Theater", "Wine Cellar", "Sky Lounge", "Concierge", "Spa & Wellness"],
        "images": ["https://via.placeholder.com/800x600/F39C12/FFFFFF?text=Lansum+Lucent"],
        "supports_group_buying": "true",
        "group_discount_percentage": "11"
    },
    {
        "name": "Aliens Corporate Towers",
        "builder_name": "Aliens Group",
        "location": "Financial District",
        "latitude": "17.4180",
        "longitude": "78.3345",
        "configuration": "3BHK",
        "carpet_area": "1750",
        "price": 125000000,  # 12.5 Cr
        "price_per_sqft": "7143",
        "description": "Tech-forward homes for executives",
        "amenities": ["AI Automation", "Voice Control", "Business Center", "Gym", "Swimming Pool", "EV Charging"],
        "images": ["https://via.placeholder.com/800x600/F39C12/FFFFFF?text=Aliens+Corporate"],
        "supports_group_buying": "true",
        "group_discount_percentage": "8"
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
                    images=prop_data.get("images", []),
                    supports_group_buying=prop_data.get("supports_group_buying", "false"),
                    group_discount_percentage=prop_data.get("group_discount_percentage"),
                    smart_score=0.0,  # Will be calculated later
                    location_score=0.0,
                    builder_score=0.0,
                    price_score=0.0,
                    commute_score=0.0
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
