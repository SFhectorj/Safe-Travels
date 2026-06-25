from core.route_logic import find_best_routes
import argparse
import sys
from database.db_handler import get_saved_location, log_route, get_route_history


def display_history(user_id):
    print("\n[System] Retrieving your recent safe routes...")
    history = get_route_history(user_id)

    if not history:
        print("No route history found.\n")
        return

    print(f"\n{'ID':<5} | {'Date':<12} | {'Destination':<25} | {'Hazards Avoided'}")
    print("-" * 65)
    for row in history:
        print(f"{row['route_id']:<5} | {str(row['date']):<12} | {row['end_location']:<25} | {row['hazards_avoided']}")
    print()


def calculate_route(user_id, start_input, end_input):
    print("\n[System] Authenticating APIs... Success.")

    actual_start = get_saved_location(user_id, start_input) + ", Los Angeles, CA"
    actual_end = get_saved_location(user_id, end_input) + ", Los Angeles, CA"

    print(f"[System] Planning route from: '{actual_start}' to '{actual_end}'")
    print("[System] Fetching pedestrian routes from Maps API...")
    print("[System] Cross-referencing routes with local Hazard API...\n")

    results = find_best_routes(actual_start, actual_end)
    quickest = results["quickest"]
    safest = results["safest"]

    print("RESULTS:")
    print(f"Route A (Fastest): {quickest['distance_m']:.0f} m | {quickest['duration_s']/60:.0f} mins | Hazard Score: {quickest['hazard_score']}/10")
    print(f"Route B (Safest):  {safest['distance_m']:.0f} m | {safest['duration_s']/60:.0f} mins | Hazard Score: {safest['hazard_score']}/10")
    print("\nRECOMMENDED PATH: Route B (Safest)")

    show = input("\n> Would you like to see turn-by-turn directions? (y/n): ").strip().lower()
    if show == 'y':
        print("\n--- Route A (Fastest) Directions ---")
        for i, step in enumerate(quickest["directions"], 1):
            print(f"   {i}. {step}")
        print("\n--- Route B (Safest) Directions ---")
        for i, step in enumerate(safest["directions"], 1):
            print(f"   {i}. {step}")

    choice = input("\n> Would you like to accept Route B and save it to your history? (y/n): ").strip().lower()

    if choice == 'y':
        log_route(user_id, actual_end, hazards_avoided=safest["total_incidents"])
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
