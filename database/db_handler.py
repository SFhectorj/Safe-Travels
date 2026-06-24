import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
  return mysql.connector.connect(
    host = os.getenv("DB_HOST"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    database = os.getenv("DB_NAME")
  )

def get_saved_location(user_id, alias):
  '''
  Looks up a saved location alias for a user in the database.
  
  If the alias exists in the user's saved locations, the corresponding
  address is returned. If no matching alias is found, the original 
  alias string is returned unchanged.
  '''
  conn = get_db_connection()
  cursor = conn.cursor(dictionary=True)

  query = "SELECT address FROM saved_locations WHERE user_id = %s AND alias = %s;"
  cursor.execute(query, (user_id, alias))
  result = cursor.fetchone()

  cursor.close()
  conn.close()

  # if no alias found return the original input
  if result:
    return result['address']
  else:
    return alias

if __name__ == "__main__":
    conn = get_db_connection()
    if conn.is_connected():
        print("[System] Successfully connected to MySQL database.")
        conn.close()
