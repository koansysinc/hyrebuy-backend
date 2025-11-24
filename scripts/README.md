# Database Seed Scripts

## Overview

These scripts populate the HyreBuy database with initial data for Phase 1 development and testing.

## Scripts

### 1. `seed_gcc_companies.py` (P1-F08)
Seeds 10 major GCC (Global Capability Center) companies in Hyderabad.

**Data**:
- Amazon, Google, Microsoft, Apple, Meta, Salesforce, Qualcomm, Oracle, Deloitte, Accenture
- Each company includes: name, location, office address, latitude, longitude, employee count

**Run**:
```bash
cd /home/koans/projects/hyrebuy/hyrebuy-backend
python scripts/seed_gcc_companies.py
```

### 2. `seed_builders.py`
Seeds 10 major real estate builders/developers in Hyderabad.

**Data**:
- Aparna Constructions, My Home Group, Aliens Group, Ramky Estates, Prestige Group, etc.
- Each builder includes: name, description, rating, on-time delivery %, group buying support

**Run**:
```bash
python scripts/seed_builders.py
```

### 3. `seed_properties.py` (P1-F04)
Seeds 13 real properties across Hyderabad.

**Locations**:
- Gachibowli (5 properties)
- Kondapur (2 properties)
- Madhapur (2 properties)
- Hitech City (2 properties)
- Manikonda (2 properties)

**Data**:
- Each property includes: name, builder, location, price (₹4.8Cr - ₹15.5Cr), configuration (2/3/4 BHK), carpet area, lat/long, amenities, group buying support

**Dependencies**: Requires builders to be seeded first (uses builder IDs)

**Run**:
```bash
python scripts/seed_properties.py
```

### 4. `seed_all.py` (Master Script)
Runs all seed scripts in the correct order.

**Order**:
1. GCC Companies
2. Builders
3. Properties

**Run**:
```bash
python scripts/seed_all.py
```

## Prerequisites

### 1. Database Setup
Ensure PostgreSQL is running and migrations are applied:

```bash
# Apply migrations
alembic upgrade head
```

### 2. Environment Variables
Ensure `.env` file has correct database connection string:

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/hyrebuy
```

### 3. Python Dependencies
All required packages should be installed:

```bash
pip install -r requirements.txt
```

## Usage

### First Time Setup
Run the master script to seed all data at once:

```bash
cd /home/koans/projects/hyrebuy/hyrebuy-backend
python scripts/seed_all.py
```

**Expected Output**:
```
======================================================================
HYREBUY DATABASE SEEDING - DAY 6
======================================================================

This will seed:
  - 10 GCC Companies (P1-F08)
  - 10 Builders
  - 13 Properties (P1-F04)

======================================================================

[Step 1/3] Seeding GCC Companies...
🏢 Seeding GCC companies...
  ✅ Added: Amazon Development Centre (Gachibowli)
  ✅ Added: Google India (Gachibowli)
  ...
✅ Successfully seeded 10 GCC companies!

[Step 2/3] Seeding Builders...
🏗️  Seeding builders...
  ✅ Added: Aparna Constructions (Rating: 4.5)
  ✅ Added: My Home Group (Rating: 4.6)
  ...
✅ Successfully seeded 10 builders!

[Step 3/3] Seeding Properties...
🏠 Seeding properties...
  ✅ Added: Aparna Sarovar Zenith - 3BHK @ ₹9.5Cr (Gachibowli)
  ✅ Added: My Home Bhooja - 3BHK @ ₹12.0Cr (Gachibowli)
  ...
✅ Successfully seeded 13/13 properties!

======================================================================
✅ ALL SEED SCRIPTS COMPLETED SUCCESSFULLY!
======================================================================

Database seeded with:
  ✅ 10 GCC Companies
  ✅ 10 Builders
  ✅ 13 Properties

Ready for Week 2 development!
======================================================================
```

### Individual Scripts
Run individual scripts if you only need specific data:

```bash
# Seed only companies
python scripts/seed_gcc_companies.py

# Seed only builders
python scripts/seed_builders.py

# Seed only properties (requires builders first)
python scripts/seed_builders.py && python scripts/seed_properties.py
```

## Data Summary

### GCC Companies (10)
| Company | Location | Employee Count |
|---------|----------|----------------|
| Amazon | Gachibowli | 15,000 |
| Google | Gachibowli | 8,000 |
| Microsoft | Gachibowli | 12,000 |
| Apple | Hitech City | 5,000 |
| Meta | Gachibowli | 3,000 |
| Salesforce | Gachibowli | 2,500 |
| Qualcomm | Hitech City | 4,000 |
| Oracle | Gachibowli | 6,000 |
| Deloitte | Gachibowli | 8,000 |
| Accenture | Gachibowli | 10,000 |

### Builders (10)
| Builder | Rating | On-Time Delivery | Group Buying |
|---------|--------|------------------|--------------|
| Aparna Constructions | 4.5 | 92% | Yes (min 5) |
| My Home Group | 4.6 | 95% | Yes (min 8) |
| Aliens Group | 4.3 | 88% | Yes (min 10) |
| Ramky Estates | 4.2 | 85% | Yes (min 6) |
| Prestige Group | 4.7 | 96% | Yes (min 12) |
| Kolte-Patil | 4.4 | 90% | Yes (min 7) |
| Hallmark Builders | 4.1 | 83% | Yes (min 5) |
| Incor Group | 4.5 | 91% | Yes (min 10) |
| Vasavi Group | 4.3 | 87% | Yes (min 6) |
| Lansum Properties | 4.2 | 86% | Yes (min 8) |

### Properties (13)
| Property | Builder | Location | Config | Price |
|----------|---------|----------|--------|-------|
| Aparna Sarovar Zenith | Aparna | Gachibowli | 3BHK | ₹9.5Cr |
| My Home Bhooja | My Home | Gachibowli | 3BHK | ₹12Cr |
| Aliens Space Station | Aliens | Gachibowli | 2BHK | ₹6.5Cr |
| Prestige Lakeside | Prestige | Kondapur | 3BHK | ₹11Cr |
| Ramky One Galaxy | Ramky | Kondapur | 2BHK | ₹5.8Cr |
| My Home Avatar | My Home | Madhapur | 3BHK | ₹11.5Cr |
| Kolte-Patil iTowers | Kolte-Patil | Madhapur | 2BHK | ₹6.2Cr |
| Aparna Cyber Life | Aparna | Hitech City | 3BHK | ₹9.8Cr |
| Incor One City | Incor | Hitech City | 4BHK | ₹15.5Cr |
| Hallmark Tranquil | Hallmark | Manikonda | 2BHK | ₹4.8Cr |
| Vasavi Usharam | Vasavi | Manikonda | 3BHK | ₹8.2Cr |
| Lansum Etania | Lansum | Gachibowli | 3BHK | ₹10.5Cr |
| Aparna Sarovar Grande | Aparna | Gachibowli | 2BHK | ₹7.2Cr |

**Price Range**: ₹4.8Cr - ₹15.5Cr
**Configurations**: 2BHK, 3BHK, 4BHK
**All properties support group buying**: 6-12% discounts

## Troubleshooting

### Error: "No module named 'app'"
**Solution**: Run scripts from backend root directory:
```bash
cd /home/koans/projects/hyrebuy/hyrebuy-backend
python scripts/seed_all.py
```

### Error: "password authentication failed"
**Solution**: Check DATABASE_URL in `.env` file

### Error: "relation does not exist"
**Solution**: Apply migrations first:
```bash
alembic upgrade head
```

### Error: "No builders found in database"
**Solution**: Seed builders before properties:
```bash
python scripts/seed_builders.py
python scripts/seed_properties.py
```

## Validation

After seeding, verify data in database:

```sql
-- Check counts
SELECT COUNT(*) FROM gcc_companies;  -- Should be 10
SELECT COUNT(*) FROM builders;       -- Should be 10
SELECT COUNT(*) FROM properties;     -- Should be 13

-- View sample data
SELECT name, location FROM gcc_companies LIMIT 5;
SELECT name, rating FROM builders LIMIT 5;
SELECT name, configuration, price FROM properties LIMIT 5;
```

## Day 6 Features Complete

- ✅ **P1-F08**: GCC Company Seeding (10 companies)
- ✅ **P1-F04**: Property Database Seeding (13 properties, partial completion)

**Note**: Day 7 will add more properties to reach the 50+ target.

---

**Status**: Day 6 seed scripts ready for execution
