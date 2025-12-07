\
\
\
   
import json
import os
import psycopg2
from datetime import datetime


def lambda_handler(event, context):
\
\
\
\
\
\
\
\
\
\
       
    
                                              
    db_host = os.environ.get('DB_HOST')
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    
    try:
                             
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        cursor = conn.cursor()
        
                     
        if isinstance(event, str):
            event_data = json.loads(event)
        else:
            event_data = event
        
                      
        cursor.execute("""
            INSERT INTO events (user_id, event_type, event_data, session_duration, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            event_data['user_id'],
            event_data['event_type'],
            json.dumps(event_data.get('event_data', {})),
            event_data.get('session_duration'),
            datetime.now()
        ))
        
                                   
        cursor.execute("""
            UPDATE users
            SET last_active = %s
            WHERE user_id = %s
        """, (datetime.now(), event_data['user_id']))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Event processed successfully',
                'event_id': cursor.lastrowid
            })
        }
    
    except Exception as e:
        print(f"Error processing event: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
