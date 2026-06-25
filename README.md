# Safe Travels

A command-line tool that helps pedestrians in Los Angeles find the safest walking route to their destination by cross-referencing real-time LAPD crime data against available walking paths.

> "1 in 5 pedestrian fatalities occur at night, yet most navigation apps only optimize for speed." — NHTSA

---

## The Problem

Many people, such as late-night workers, students, and vulnerable community members, must walk to their destinations in large cities. Standard navigation apps prioritize the fastest route, not the safest. Safe Travels advocates for pedestrians by surfacing crime data alongside route options so users can make an informed choice.

---

## Features

- Generates up to 3 walking route options using the OpenRouteService API
- Scores each route using live LAPD crime data (2020–present)
- Recommends the safest route with a 0–10 hazard score
- Saves completed routes to a personal history log

---

## Tech Stack

| Component | Technology |
|---|---|
| Mapping API | OpenRouteService (foot-walking) |
| Crime Data API | LAPD Crime Data via Socrata SODA API |
| Database | MySQL (3NF schema) |
| Language | Python 3 |
| Interface | CLI (argparse) |

---

## Setup

### 1. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Set environment variables
Create a `.env` file in the project root (or use Codio's environment variable settings):
```
ORS_API_KEY=your_openrouteservice_key
LA_CRIME_APP_TOKEN=your_socrata_app_token
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=safe_travels_db
```

### 3. Set up the database
### 4. Create package init files (if not present)


---

## Usage

**Find a route:**
```bash
python3 main.py -s "Hollywood" -e "Koreatown"
```

**Use a saved location alias:**
```bash
python3 main.py -s "Home" -e "Library"
```

**View route history:**
```bash
python3 main.py --history
python3 main.py --history -u 2
```

**Help:**
```bash
python3 main.py --help
```

---

## Run Tests
```bash
python3 -m pytest tests/test_functions.py -v
```

---

## File Structure

```
safe-travels/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py                  # CLI entry point
├── api/
│   ├── maps_client.py       # OpenRouteService API
│   └── hazard_client.py     # LAPD Crime Data API
├── core/
│   └── route_logic.py       # Route scoring and comparison
├── database/
│   ├── schema.sql           # 3NF database schema
│   └── db_handler.py        # SQL query functions
└── tests/
    └── test_functions.py    # Unit tests
```

---

## Version 2 Ideas

- TBD