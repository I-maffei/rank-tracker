import requests
import json
import datetime
import os

API_KEY = os.environ.get("SERPAPI_KEY")
TARGET_URL = "maffei-structure.com/work/san-francisco-concrete-building-screening-program/"

QUERIES = [
    "concrete building screening program",
    "concrete building screening",
    "concrete screening",
]

LOCATIONS = [
    {"name": "San Francisco, CA", "location": "San Francisco, California, United States"},
    {"name": "California",        "location": "California, United States"},
]

# --- Step 1: Fetch rankings and append to rank_history.json ---

for loc in LOCATIONS:
    for query in QUERIES:
        params = {
            "q": query,
            "api_key": API_KEY,
            "num": 100,
            "location": loc["location"],
            "hl": "en",
            "gl": "us",
        }
        results = requests.get("https://serpapi.com/search", params=params).json()

        rank = None
        for i, result in enumerate(results.get("organic_results", []), start=1):
            if TARGET_URL in result.get("link", ""):
                rank = i
                break

        entry = {
            "date": str(datetime.date.today()),
            "location": loc["name"],
            "query": query,
            "rank": rank,
            "url": TARGET_URL,
        }

        print(f"[{loc['name']}] '{query}' -> Rank: {rank if rank else 'Not in top 100'}")

        with open("rank_history.json", "a") as f:
            f.write(json.dumps(entry) + "\n")

print("Results saved to rank_history.json")

# --- Step 2: Load all history and generate rank_tracker.html ---

all_data = []
with open("rank_history.json", "r") as f:
    for line in f:
        line = line.strip()
        if line:
            try:
                all_data.append(json.loads(line))
            except json.JSONDecodeError:
                pass

data_json = json.dumps(all_data)

html_template = open(os.path.join(os.path.dirname(__file__), "rank_template.html")).read()
html = html_template.replace("__DATA_JSON__", data_json)

with open("rank_tracker.html", "w") as f:
    f.write(html)

print("Visualization saved to rank_tracker.html")
