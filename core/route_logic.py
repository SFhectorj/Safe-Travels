import polyline as pl 
from api.maps_client import get_alternative_routes
from api.hazard_client import get_route_hazard_score

def decode_geometry(encoded):
    return pl.decode(encoded, precision=5)

def sample_waypoints(coords, n=8):
    if len(coords) <=n:
        return coords
    step = max(1,len(coords)//n)
    return coords[::step]
def find_best_routes(start,end):
    routes = get_alternative_routes(start,end)
    print(f"ORS returned {len(routes)} route(s)")


    for route in routes:
        coords = decode_geometry(route["geometry"])
        waypoints = sample_waypoints(coords)
        hazard = get_route_hazard_score(waypoints)
        route["hazard_score"] = hazard["average_score"]
        route["total_incidents"] = hazard["total_incidents"]
    quickest = min(routes, key= lambda r: r["duration_s"])
    safest = min(routes, key = lambda r: r["hazard_score"])
    return {"quickest": quickest, "safest": safest}
