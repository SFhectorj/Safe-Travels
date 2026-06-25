import os
import requests
from datetime import datetime, timedelta

LA_CRIME_API_URL = "https://data.lacity.org/resource/y8y3-fqfu.json"


LOOKBACK_DAYS = 730
SCORE_CAP = 40

WEIGHTS = {
  "person_crime": 3,
  "weapon": 2,
  "shot_victim": 5,
  "gang_related": 2,
  "hate_crime": 1,
  "base": 1,
}

def cutoff_date():
  cutoff = datetime.utcnow()- timedelta(days=LOOKBACK_DAYS)
  return cutoff.strftime("%Y-%m-%dT%H:%M:%S.000")

def get_crimes_near_point(lat, lon, radius_m = 150, limit=50):
  app_token = os.getenv("LA_CRIME_APP_TOKEN")

  delta_lat = radius_m / 111000
  delta_lon = radius_m / 92500

  where = (
    f"lat >= '{lat - delta_lat}' AND lat <= '{lat + delta_lat}' AND "
    f"lon >= '{lon - delta_lon}' AND lon <= '{lon + delta_lon}' AND "
    f"date_occ >= '{cutoff_date()}'"
  )
  headers = {"X-App-Token": app_token} if app_token else {}
  params = {"$where": where,"$limit":limit,"$order":"date_occ DESC"}

  response = requests.get(LA_CRIME_API_URL, params=params, headers=headers)
  response.raise_for_status()
  return response.json()

MAX_SEVERITY = sum(WEIGHTS.values())
def compute_hazard_score(crimes):
  if not crimes:
      return 0.0
  total = 0
  for c in crimes:
      s = WEIGHTS["base"]
      if c.get("crime_against", "").lower() == "person":
          s += WEIGHTS["person_crime"]
      if c.get("weapon_used_cd"):
          s += WEIGHTS["weapon"]
      if c.get("victim_shot", "No").lower() == "yes":
          s += WEIGHTS["shot_victim"]
      if c.get("gang_related_crime", "No").lower() == "yes":
          s += WEIGHTS["gang_related"]
      if c.get("hate_crime", "No").lower() == "yes":
          s += WEIGHTS["hate_crime"]
      total+=s
  avg = total / len(crimes)
  return round((avg / MAX_SEVERITY) * 10, 2)
def score_waypoint(waypoints, radius_m=150):
  res = []
  for lat, lon in waypoints:
    crimes = get_crimes_near_point(lat,lon,radius_m=radius_m)
    score = compute_hazard_score(crimes)
    res.append({"lat": lat, "lon": lon, "score": score, "incident_count": len(crimes)})
  return res

def get_route_hazard_score(waypoints,radius_m=150):
  if not waypoints:
    return {"average_score": 0.0, "max_score": 0.0, "total_incidents": 0, "waypoint_scores": []}
  scored = score_waypoint(waypoints,radius_m=radius_m)
  scores = [w["score"] for w in scored]
  total_incidents = sum(w["incident_count"] for w in scored)

  return {
    "average_score": round(sum(scores) / len(scores), 2),
    "max_score": max(scores),
    "total_incidents": total_incidents,
    "waypoint_scores": scored,
  }


