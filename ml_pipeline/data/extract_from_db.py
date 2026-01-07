import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()


def extract_data_from_db(database_url: str = None) -> tuple[pd.DataFrame, pd.DataFrame]:
\
\
\
\
\
       
    if database_url is None:
        database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/analytics')
    
    engine = create_engine(database_url)
    
                   
    users_query = """
    SELECT 
        user_id,
        email,
        created_at,
        last_active,
        subscription_tier,
        churned,
        churn_date
    FROM users
    """
    users_df = pd.read_sql(users_query, engine)
    
                    
    events_query = """
    SELECT 
        event_id,
        user_id,
        event_type,
        event_data,
        session_duration,
        timestamp
    FROM events
    """
    events_df = pd.read_sql(events_query, engine)
    
    engine.dispose()
    
    print(f"Extracted {len(users_df)} users and {len(events_df)} events")
    
    return users_df, events_df


def save_data_to_csv(users_df: pd.DataFrame, events_df: pd.DataFrame, output_dir: str = "./data"):
\
\
       
    os.makedirs(output_dir, exist_ok=True)
    
    users_df.to_csv(f"{output_dir}/users.csv", index=False)
    events_df.to_csv(f"{output_dir}/events.csv", index=False)
    
    print(f"Data saved to {output_dir}/")


if __name__ == "__main__":
    users_df, events_df = extract_data_from_db()
    save_data_to_csv(users_df, events_df)
