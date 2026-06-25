import argparse
import Sys
from database.db_handler import get_saved_location, log_route, get_route_history

def display_history(user_id):
  '''
  Retrieves and displays the user's five most recent routes
  in a formatted table, including destination, date, and hazards avoided.
  '''

  print("\n[System] Retrieving your recent safe routes...")
  history = get_route_history(user_id)

  if not history:
    print("No route history(user_id)")
    return
    
  # Format table
  print(f"\n{'ID':<5} | {'Date':<12} | {'Destination':<25} | {'Hazards Avoided'}")
  print("-" * 65)
  
  # Loop through routes and print
  for row in history:
    print(f"{row['route_id']:<5} | {str(row['date']):<12} | {row['end_location']:<25} | {row['hazards_avoided']}")
    print("\n")

