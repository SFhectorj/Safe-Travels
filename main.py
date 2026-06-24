from api.maps_client import geocode_city, get_route

def main():
    lon,lat = geocode_city("Los Angeles")
    print("Los Angeles coords:", lon, lat)

    route = get_route("Los Angeles", "Irvine")
    print("Distance (m):", route["distance_m"])
    print("Duration (s):", route["duration_s"])
    #print("Geometry (first 100 chars):", route["geometry"][:100])
    print("\nTurn‑by‑turn directions:")
    for i, line in enumerate(route["directions"], start=1):
        print(f"{i}. {line}")
if __name__ == "__main__":
    main()