import argparse
import sys
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

def calculate_route(user_id, start_input, end_input):
  '''
  routing logic and database logging
  Currently outputs DEMO
  '''

  print("\n[System] Authenticating APIs... Success.")

  # Check database for saved locations
  actual_start = get_saved_location(user_id, start_input)
  actual_end = get_saved_location(user_id, end_input)
  
  print(f"[System] Planning route from: '{actual_start}' to '{actual_end}'")
  # DEMO Output
  print("[System] Fetching pedestrian routes from Maps API... (STUB)")
  print("[System] Cross-referencing routes with local Hazard API... (STUB)\n")

  # DEMO Output
  print("RESULTS:")
  print("Route A (Fastest): 0.6 miles | 12 mins | WARNING: 2 recent incident reports.")
  print("Route B (Safest):  0.8 miles | 16 mins | STATUS: Clear. Well-lit streets.\n")
  print("RECOMMENDED PATH: Route B")

  # Request user input 
  choice = input("> Would you like to accept Route B and save it to your history? (y/n): ").strip().lower()

  if choice == 'y':
    # DEMO Output: logging hazards avoided
    log_route(user_id, actual_end, hazards_avoided=2)
    print("[System] Route successfully saved to database. Stay safe!\n")
  else:
    print("[System] Route discarded.\n")

def main():
  parser = argparse.ArgumentParser(
    prog="Safe-Travels",
    description="Peace of mind when out and about."
  )
  
  parser.add_argument("-s", "--start", type=str, help="Starting location or saved alias (e.g., 'Library')")
  parser.add_argument("-e", "--end", type=str, help="Destination location")
  parser.add_argument("--history", action="store_true", help="View your past safe routes")
  parser.add_argument("-u", "--user", type=int, default=1, help="User ID (defaults to 1 for testing)")

  args = parser.parse_args()

  if args.history:
    display_history(args.user)
  elif args.start and args.end:
    calculate_route(args.user, args.start, args.end)
  else:
    parser.print_help()
    sys.exit(1)

if __name__ == "__main__":
    main()
