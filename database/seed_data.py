\
\
   
import psycopg2
from psycopg2.extras import execute_values
import random
from datetime import datetime, timedelta
from faker import Faker
import os
from dotenv import load_dotenv

load_dotenv()

fake = Faker()
Faker.seed(42)
random.seed(42)

                               
EVENT_TYPES = [
    'login',
    'page_view',
    'feature_usage',
    'purchase',
    'support_ticket',
    'settings_change',
    'export_data',
    'share_content',
    'api_call',
    'logout'
]

SUBSCRIPTION_TIERS = ['free', 'basic', 'premium', 'enterprise']


def get_db_connection():
                                    
    database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/analytics')
    
                             
                                                           
    parts = database_url.replace('postgresql://', '').split('@')
    user_pass = parts[0].split(':')
    host_port_db = parts[1].split('/')
    host_port = host_port_db[0].split(':')
    
    conn = psycopg2.connect(
        host=host_port[0],
        port=int(host_port[1]) if len(host_port) > 1 else 5432,
        database=host_port_db[1],
        user=user_pass[0],
        password=user_pass[1]
    )
    
    return conn


def generate_users(n_users=1000):
                                  
    users = []
    
    for i in range(n_users):
                                                       
        will_churn = random.random() < 0.3
        
        created_at = fake.date_time_between(start_date='-2y', end_date='-1m')
        
        if will_churn:
                                                       
            last_active = datetime.now() - timedelta(days=random.randint(30, 90))
            churned = True
            churn_date = last_active + timedelta(days=random.randint(1, 7))
        else:
                                                           
            last_active = datetime.now() - timedelta(days=random.randint(0, 30))
            churned = False
            churn_date = None
        
                                                                       
        if churned:
            tier = random.choices(
                SUBSCRIPTION_TIERS,
                weights=[0.6, 0.25, 0.1, 0.05]
            )[0]
        else:
            tier = random.choices(
                SUBSCRIPTION_TIERS,
                weights=[0.3, 0.3, 0.25, 0.15]
            )[0]
        
        users.append((
            fake.unique.email(),
            created_at,
            last_active,
            tier,
            churned,
            churn_date
        ))
    
    return users


def generate_events(users, conn):
                                             
    cursor = conn.cursor()
    
                  
    cursor.execute("SELECT user_id, last_active, churned FROM users")
    user_data = cursor.fetchall()
    
    events = []
    
    for user_id, last_active, churned in user_data:
        if churned:
                                                           
            n_events = random.randint(5, 50)
            session_duration_range = (1, 10)           
        else:
                                                          
            n_events = random.randint(50, 500)
            session_duration_range = (5, 60)           
        
                                                
        for _ in range(n_events):
                                                                   
            days_ago = random.randint(0, 365)
            event_time = last_active - timedelta(days=days_ago)
            
                        
            event_type = random.choice(EVENT_TYPES)
            
                              
            session_duration = random.uniform(*session_duration_range)
            
                               
            event_data = {
                'source': random.choice(['web', 'mobile', 'api']),
                'browser': random.choice(['chrome', 'firefox', 'safari', 'edge']),
                'device': random.choice(['desktop', 'mobile', 'tablet'])
            }
            
            events.append((
                user_id,
                event_type,
                str(event_data).replace("'", '"'),
                session_duration,
                event_time
            ))
    
    return events


def seed_database():
                               
    print("=" * 60)
    print("Seeding Database with Synthetic Data")
    print("=" * 60)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
                         
    print("\n1. Clearing existing data...")
    cursor.execute("TRUNCATE users, events, predictions, model_metadata RESTART IDENTITY CASCADE")
    conn.commit()
    
                               
    print("\n2. Generating users...")
    users = generate_users(n_users=1000)
    
    print(f"   Generated {len(users)} users")
    print("   Inserting into database...")
    
    execute_values(
        cursor,
        """
        INSERT INTO users (email, created_at, last_active, subscription_tier, churned, churn_date)
        VALUES %s
        """,
        users
    )
    conn.commit()
    print("   ✓ Users inserted")
    
                                
    print("\n3. Generating events...")
    events = generate_events(users, conn)
    
    print(f"   Generated {len(events)} events")
    print("   Inserting into database...")
    
                       
    batch_size = 1000
    for i in range(0, len(events), batch_size):
        batch = events[i:i + batch_size]
        execute_values(
            cursor,
            """
            INSERT INTO events (user_id, event_type, event_data, session_duration, timestamp)
            VALUES %s
            """,
            batch
        )
        print(f"   Inserted batch {i // batch_size + 1}/{(len(events) + batch_size - 1) // batch_size}")
    
    conn.commit()
    print("   ✓ Events inserted")
    
                                   
    print("\n4. Inserting initial model metadata...")
    cursor.execute("""
        INSERT INTO model_metadata (version, accuracy, deployed_at, storage_path, is_active)
        VALUES ('v0.0.0', 0.0, NOW(), 'models/initial', FALSE)
        ON CONFLICT (version) DO NOTHING
    """)
    conn.commit()
    print("   ✓ Model metadata inserted")
    
                      
    print("\n" + "=" * 60)
    print("Database Statistics:")
    print("=" * 60)
    
    cursor.execute("SELECT COUNT(*) FROM users")
    print(f"Total users: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE churned = TRUE")
    print(f"Churned users: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM events")
    print(f"Total events: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT subscription_tier, COUNT(*) FROM users GROUP BY subscription_tier")
    print("\nUsers by subscription tier:")
    for tier, count in cursor.fetchall():
        print(f"  {tier}: {count}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✓ Database seeding complete!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        seed_database()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
