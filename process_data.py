import csv
import json
import urllib.parse
from datetime import datetime, timedelta
import os

OUTPUT = os.path.join(os.path.dirname(__file__), 'output')
DATA = os.path.join(OUTPUT, 'data')

def log_activity(message):
    path = os.path.join(DATA, 'activity.json')
    with open(path) as f:
        activity = json.load(f)
    activity['events'].insert(0, {
        'timestamp': datetime.now().isoformat(),
        'message': message
    })
    with open(path, 'w') as f:
        json.dump(activity, f, indent=2)
    print(f"[LOG] {message}")

def maps_link(name, address, city):
    q = f"{name} {address} {city} CA".strip()
    return f"https://www.google.com/maps/search/{urllib.parse.quote_plus(q)}"

# Non-restaurant keywords to filter out
EXCLUDE_KEYWORDS = [
    'swimming pool', 'public swimming', 'apartment', 'mobile home',
    'motel', 'hotel', 'school cafeteria', 'public school', 'private school',
    'recovery', 'body art', 'tattoo', 'interim housing', 'condo',
    'remote storage', 'wading pool'
]

INCLUDE_KEYWORDS = [
    'restaurant', 'food mkt', 'bakery', 'bar', 'cafeteria', 'food truck',
    'cafe', 'grill', 'pizza', 'burger', 'taco', 'diner', 'buffet',
    'seats', 'food market', 'food mkt retail'
]

def is_restaurant(description):
    desc = description.lower()
    for kw in EXCLUDE_KEYWORDS:
        if kw in desc:
            return False
    for kw in INCLUDE_KEYWORDS:
        if kw in desc:
            return True
    return False

def process_closures():
    log_activity("Starting closure data processing...")

    # Read the raw closure CSV from the user's pasted data
    raw_path = os.path.join(os.path.dirname(__file__), 'closures_raw.csv')
    if not os.path.exists(raw_path):
        log_activity("ERROR: closures_raw.csv not found")
        return

    closures = []
    with open(raw_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            address = row.get('Address', '').strip()
            city = row.get('City', '').strip()
            description = row.get('Description', '').strip()
            closed = row.get('Closed', '').strip()
            reopened = row.get('Reopened', '').strip()
            reason = row.get('Reason', '').strip()

            # Skip if already reopened
            if reopened:
                continue

            # Skip if no closed date
            if not closed:
                continue

            # Skip non-restaurant facilities
            if not is_restaurant(description):
                continue

            closures.append({
                'facility_name': name,
                'address': address,
                'city': city,
                'description': description,
                'closed_date': closed,
                'reopened_date': None,
                'reason': reason,
                'google_maps_link': maps_link(name, address, city)
            })

    # Write JSON for dashboard
    json_out = {
        'last_scrape': datetime.now().isoformat(),
        'closures': closures
    }
    with open(os.path.join(DATA, 'closures.json'), 'w') as f:
        json.dump(json_out, f, indent=2)

    # Write CSV
    csv_path = os.path.join(OUTPUT, 'closures.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Facility Name', 'Address', 'City', 'Description', 'Closed Date', 'Reason', 'Google Maps Link'])
        for c in closures:
            writer.writerow([c['facility_name'], c['address'], c['city'], c['description'], c['closed_date'], c['reason'], c['google_maps_link']])

    log_activity(f"Closures processed: {len(closures)} still-closed restaurants found (filtered from raw data)")

def process_inspections():
    log_activity("Starting inspection score processing...")

    raw_path = os.path.join(os.path.dirname(__file__), 'inspections.csv')
    if not os.path.exists(raw_path):
        log_activity("ERROR: inspections.csv not found")
        return

    # No header in this CSV — columns are: Name, Date, Score, Address, City, ID
    cutoff = datetime.now() - timedelta(days=7)
    low_scores = []

    with open(raw_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 6:
                continue
            name = row[0].strip()
            date_str = row[1].strip()
            try:
                score = int(row[2].strip())
            except (ValueError, IndexError):
                continue
            address = row[3].strip()
            city = row[4].strip()

            # Parse date
            try:
                insp_date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                continue

            # Only last 7 days
            if insp_date < cutoff:
                continue

            # Only below 90
            if score >= 90:
                continue

            # Determine grade
            if score >= 80:
                grade = 'B'
            else:
                grade = 'C'

            low_scores.append({
                'facility_name': name,
                'address': address,
                'city': city,
                'inspection_date': date_str,
                'score': score,
                'grade': grade,
                'google_maps_link': maps_link(name, address, city)
            })

    # Write JSON for dashboard
    json_out = {
        'last_scrape': datetime.now().isoformat(),
        'low_scores': low_scores
    }
    with open(os.path.join(DATA, 'low_scores.json'), 'w') as f:
        json.dump(json_out, f, indent=2)

    # Write CSV
    csv_path = os.path.join(OUTPUT, 'low_scores.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Facility Name', 'Address', 'City', 'Inspection Date', 'Score', 'Grade', 'Google Maps Link'])
        for s in low_scores:
            writer.writerow([s['facility_name'], s['address'], s['city'], s['inspection_date'], s['score'], s['grade'], s['google_maps_link']])

    log_activity(f"Inspections processed: {len(low_scores)} restaurants scored below 90 in the last 7 days")

if __name__ == '__main__':
    log_activity("=== Data processing started ===")
    process_closures()
    process_inspections()
    log_activity("=== Data processing complete. Dashboard updated. ===")
