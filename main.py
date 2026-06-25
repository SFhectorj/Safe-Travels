from api.maps_client import geocode_city, get_route
from api.hazard_client import get_crimes_near_point, compute_hazard_score
from core.route_logic import find_best_routes
import argparse
import sys
from database.db_handler import get_saved_location, log_route, get_route_history


#Kamsi's test logic
def main():
    start = input("Enter start location: ") + ", Los Angeles, CA"
    end = input("Enter destination: ") + ", Los Angeles, CA"

    print("\nFinding routes and checking safety along the way...\n")
    results = find_best_routes(start, end)

    quickest = results["quickest"]
    safest = results["safest"]

    print("--- QUICKEST ROUTE ---")
    print(f"Time: {quickest['duration_s'] / 60:.0f} min  |  Distance: {quickest['distance_m']:.0f} m  |  Hazard: {quickest['hazard_score']}/10")
    print("Directions:")
    # for i, step in enumerate(quickest["directions"], 1):
    #     print(f"  {i}. {step}")

    print("\n--- SAFEST ROUTE ---")
    print(f"Time: {safest['duration_s'] / 60:.0f} min  |  Distance: {safest['distance_m']:.0f} m  |  Hazard: {safest['hazard_score']}/10")
    print("Directions:")
    # for i, step in enumerate(safest["directions"], 1):
    #     print(f"  {i}. {step}")



if __name__ == "__main__":
    main()
