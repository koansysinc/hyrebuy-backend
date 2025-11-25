"""
Seed Data Script for Group Buying Feature Testing
Creates realistic test data for buying groups, members, invites, and messages
"""

import asyncio
import asyncpg
from datetime import datetime, timedelta
import uuid
import random
import string

# Database connection
DATABASE_URL = "postgres://f1061be62d163a20e0f4fd1aeeb789bacb6032c49341308e7891068696c56746:sk_fSCX2wag8FWJy4PdjSO3H@db.prisma.io:5432/postgres?sslmode=require"

# Hyderabad tech hub locations
LOCATIONS = [
    "Gachibowli", "Hitech City", "Kondapur", "Madhapur", "Financial District",
    "Kokapet", "Nanakramguda", "Manikonda", "Tellapur", "Narsingi"
]

CONFIGURATIONS = ["2BHK", "3BHK", "4BHK", "Penthouse"]

# Sample group names
GROUP_NAMES = [
    "Gachibowli Premium 3BHK Buyers",
    "Hitech City Affordable Housing Group",
    "Kondapur Luxury Villa Seekers",
    "Madhapur IT Professionals Housing",
    "Financial District Executive Homes",
    "Kokapet Smart City Residents",
    "Nanakramguda Tech Park Employees",
    "Manikonda Family Apartments",
    "Tellapur Green Living Community",
    "Narsingi Budget Homes Group"
]

GROUP_DESCRIPTIONS = [
    "Looking for premium 3BHK apartments near tech parks with excellent connectivity.",
    "Group of IT professionals seeking affordable housing with good amenities.",
    "Luxury villa seekers planning to buy spacious properties with private gardens.",
    "Tech employees coordinating bulk purchase for better pricing and terms.",
    "Executive professionals looking for high-end apartments in prime location.",
    "Early investors in the upcoming smart city project with modern infrastructure.",
    "Employees working in nearby tech parks looking for convenient housing.",
    "Families seeking safe, child-friendly apartments with schools nearby.",
    "Eco-conscious buyers interested in sustainable living projects.",
    "First-time home buyers pooling resources for better deals."
]

# Sample messages
SAMPLE_MESSAGES = [
    "Hi everyone! Excited to be part of this group. Looking forward to finding great deals together.",
    "Has anyone visited the sample flats in this area? Would love to hear your thoughts.",
    "I think we should aim for properties near the metro station. What do you all think?",
    "The builder shared some floor plans with me. Happy to share them with the group.",
    "We need 2 more members to unlock the silver tier discount. Let's invite our colleagues!",
    "Just joined! Working at Google, looking for a 3BHK within 5km of my office.",
    "I've done some research on the builder's previous projects. They seem reliable.",
    "What's our timeline? I'm looking to finalize by end of this quarter.",
    "Should we schedule a group visit to the property site next weekend?",
    "Great to see the group growing! Let's coordinate our negotiations together."
]

def generate_invite_code(length=9):
    """Generate a random invite code"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


async def create_seed_data():
    """Create comprehensive seed data for testing"""
    conn = await asyncpg.connect(DATABASE_URL)

    print("🌱 Starting seed data creation...\n")

    try:
        # Get existing users
        users = await conn.fetch('SELECT id FROM users')
        user_ids = [user['id'] for user in users]
        print(f"✓ Found {len(user_ids)} existing users")

        # Get builder IDs
        builders = await conn.fetch('SELECT id FROM builders LIMIT 5')
        builder_ids = [builder['id'] for builder in builders]
        print(f"✓ Found {len(builder_ids)} builders")

        if len(user_ids) < 2:
            print("❌ Need at least 2 users in the database. Please create users first.")
            return

        # Create additional test users
        print("\n📝 Creating additional test users...")
        new_users = []
        for i in range(8):  # Create 8 more users for a total of 10
            user_id = uuid.uuid4()
            email = f"user{i+3}@hyrebuy.com"
            name = f"Test User {i+3}"
            password_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5tdcBpZpL6whO"  # "password"

            await conn.execute('''
                INSERT INTO users (id, email, password_hash, name, phone, is_group_admin, total_rewards_earned)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT (email) DO NOTHING
            ''', user_id, email, password_hash, name, f"+9198765432{10+i}", "false", "0")

            new_users.append(user_id)

        # Refresh user list
        users = await conn.fetch('SELECT id FROM users')
        user_ids = [user['id'] for user in users]
        print(f"✓ Now have {len(user_ids)} total users")

        # Create buying groups with different statuses
        print("\n🏘️  Creating buying groups...")
        group_ids = []

        statuses = ["forming", "forming", "forming", "negotiating", "negotiating", "closed"]

        for i in range(6):
            group_id = uuid.uuid4()
            admin_id = random.choice(user_ids)
            location = LOCATIONS[i]
            config = random.choice(CONFIGURATIONS)
            status = statuses[i]

            # Determine member counts based on status
            if status == "forming":
                current_members = random.randint(2, 4)
                committed_members = random.randint(0, 2)
            elif status == "negotiating":
                current_members = random.randint(6, 10)
                committed_members = random.randint(4, current_members)
            else:  # closed
                current_members = random.randint(8, 15)
                committed_members = current_members

            # Calculate discount tier based on members
            if current_members >= 15:
                tier = "platinum"
                discount = "20.00"
            elif current_members >= 10:
                tier = "gold"
                discount = "15.00"
            elif current_members >= 5:
                tier = "silver"
                discount = "10.00"
            else:
                tier = "bronze"
                discount = "5.00"

            budget_min = random.choice([60000000, 80000000, 100000000])
            budget_max = budget_min + random.choice([20000000, 40000000, 50000000])

            invite_code = generate_invite_code()

            # Select random builders - convert UUIDs to strings for asyncpg
            selected_builders = [str(bid) for bid in random.sample(builder_ids, min(2, len(builder_ids)))]

            close_date = datetime.now() + timedelta(days=random.randint(30, 90))

            await conn.execute('''
                INSERT INTO buying_groups (
                    id, admin_id, name, description, target_location, target_configuration,
                    budget_min, budget_max, preferred_builders, minimum_members, maximum_members,
                    close_by_date, status, current_member_count, committed_member_count,
                    expected_discount_percent, current_discount_tier, selected_builder_id,
                    invite_code, is_discoverable
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20)
            ''',
                group_id, admin_id, GROUP_NAMES[i], GROUP_DESCRIPTIONS[i], location, config,
                budget_min, budget_max, selected_builders, "5", "20",
                close_date.date(), status, str(current_members), str(committed_members),
                discount, tier, random.choice(builder_ids) if status == "closed" else None,
                invite_code, "true"
            )

            group_ids.append({
                'id': group_id,
                'admin_id': admin_id,
                'current_members': current_members,
                'committed_members': committed_members,
                'status': status
            })

            print(f"  ✓ {GROUP_NAMES[i]} - {status} ({current_members} members, {tier} tier)")

        print(f"\n✓ Created {len(group_ids)} buying groups")

        # Create group members
        print("\n👥 Creating group members...")
        member_count = 0

        for group in group_ids:
            group_id = group['id']
            admin_id = group['admin_id']
            target_members = group['current_members']
            committed_count = group['committed_members']

            # Add admin as committed member
            member_id = uuid.uuid4()
            await conn.execute('''
                INSERT INTO group_members (
                    id, group_id, user_id, status, commitment_level,
                    invited_by, joined_at, committed_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ''',
                member_id, group_id, admin_id, "committed", "100",
                None, datetime.now() - timedelta(days=random.randint(10, 30)),
                datetime.now() - timedelta(days=random.randint(5, 15))
            )
            member_count += 1

            # Add other members
            available_users = [uid for uid in user_ids if uid != admin_id]
            selected_members = random.sample(available_users, min(target_members - 1, len(available_users)))

            committed_so_far = 1  # Admin is already committed

            for user_id in selected_members:
                member_id = uuid.uuid4()

                # Determine member status
                if committed_so_far < committed_count:
                    member_status = "committed"
                    commitment = random.randint(80, 100)
                    committed_at = datetime.now() - timedelta(days=random.randint(1, 10))
                    committed_so_far += 1
                else:
                    member_status = random.choice(["interested", "interested", "invited"])
                    commitment = random.randint(40, 70)
                    committed_at = None

                joined_at = datetime.now() - timedelta(days=random.randint(5, 25))

                await conn.execute('''
                    INSERT INTO group_members (
                        id, group_id, user_id, status, commitment_level,
                        invited_by, joined_at, committed_at
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ''',
                    member_id, group_id, user_id, member_status, str(commitment),
                    admin_id, joined_at, committed_at
                )
                member_count += 1

        print(f"✓ Created {member_count} group memberships")

        # Create group invites
        print("\n📧 Creating group invites...")
        invite_count = 0

        for group in group_ids[:4]:  # First 4 groups have active invites
            group_id = group['id']
            admin_id = group['admin_id']

            # Create 2-3 invites per group
            num_invites = random.randint(2, 3)

            for _ in range(num_invites):
                invite_id = uuid.uuid4()
                invite_code = generate_invite_code()
                sharing_method = random.choice(["whatsapp", "email", "link"])
                status = random.choice(["pending", "pending", "accepted"])

                # Generate WhatsApp link if sharing via WhatsApp
                whatsapp_link = None
                if sharing_method == "whatsapp":
                    invite_url = f"https://hyrebuy.com/groups/join/{invite_code}"
                    message = f"Join my property buying group on HyreBuy!"
                    whatsapp_link = f"https://wa.me/?text={message.replace(' ', '%20')}%20{invite_url}"

                await conn.execute('''
                    INSERT INTO group_invites (
                        id, group_id, inviter_id, invite_code, status,
                        sharing_method, whatsapp_link
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                ''',
                    invite_id, group_id, admin_id, invite_code, status,
                    sharing_method, whatsapp_link
                )
                invite_count += 1

        print(f"✓ Created {invite_count} group invites")

        # Create group messages
        print("\n💬 Creating group messages...")
        message_count = 0

        for group in group_ids:
            group_id = group['id']

            # Get members of this group
            members = await conn.fetch('''
                SELECT user_id FROM group_members WHERE group_id = $1
            ''', group_id)

            member_ids = [m['user_id'] for m in members]

            # Create 5-10 messages per group
            num_messages = random.randint(5, 10)

            for i in range(num_messages):
                msg_id = uuid.uuid4()
                sender_id = random.choice(member_ids)
                message_text = random.choice(SAMPLE_MESSAGES)
                created_at = datetime.now() - timedelta(days=random.randint(0, 20), hours=random.randint(0, 23))

                await conn.execute('''
                    INSERT INTO group_messages (
                        id, group_id, sender_id, message, message_type, is_pinned
                    )
                    VALUES ($1, $2, $3, $4, $5, $6)
                ''',
                    msg_id, group_id, sender_id, message_text, "text", "false"
                )
                message_count += 1

        print(f"✓ Created {message_count} group messages")

        print("\n" + "="*60)
        print("🎉 Seed data creation completed successfully!")
        print("="*60)
        print(f"""
Summary:
  - Users: {len(user_ids)} total
  - Buying Groups: {len(group_ids)}
    • Forming: 3 groups
    • Negotiating: 2 groups
    • Closed: 1 group
  - Group Members: {member_count}
  - Group Invites: {invite_count}
  - Group Messages: {message_count}

You can now test the group buying feature at:
  Frontend: http://localhost:3000/groups
  API Docs: http://localhost:8000/docs
        """)

    except Exception as e:
        print(f"\n❌ Error creating seed data: {e}")
        import traceback
        traceback.print_exc()

    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(create_seed_data())
