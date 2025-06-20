#!/usr/bin/env python3
"""
FishELF engine:
• Lists which fish are currently available
• Marks a fish as caught (after the player successfully calls it in GDB)
Usage examples
--------------
# See what's biting right now at the pond
python3 fishengine.py --zone pond

# Pretend it's 9 pm and raining at the pier
python3 fishengine.py --zone sea --location pier --weather raining \
    --override-time "2025-06-20 21:00"

# Log that we caught 'magikarp' in the pond
python3 fishengine.py --zone pond --catch magikarp
"""
import argparse, json, sys
from datetime import datetime
from pathlib import Path

DATA_FILE  = Path("fishdata.json")
SAVE_FILE  = Path("save.json")

def load_json(path):
    if not path.exists():
        print(f"[!!] {path} missing"); sys.exit(1)
    with path.open() as f:
        return json.load(f)

def save_json(path, data):
    with path.open("w") as f:
        json.dump(data, f, indent=2)

def expand_hour_rule(hrule):
    """Accept `[0,23]` (range) OR explicit hour list"""
    if len(hrule)==2:
        start, end = hrule
        return list(range(start, end+1))
    return hrule

def is_available(fish, now, weather, location):
    m = now.month
    h = now.hour
    months  = fish["months"]
    hours   = expand_hour_rule(fish["hours"])
    weather_ok  = weather in fish["weather"] or "any" in fish["weather"]
    location_ok = location in fish["location"]
    return m in months and h in hours and weather_ok and location_ok

def list_available(zone, now, weather, location, fishdata, save):
    available = []
    for name, meta in fishdata[zone].items():
        if is_available(meta, now, weather, location):
            caught = save.get(zone, {}).get(name, {}).get("caught", False)
            available.append((name, caught))
    return available

def mark_caught(zone, fishname, save):
    zone_dict = save.setdefault(zone, {})
    zone_dict[fishname] = {"caught": True,
                           "timestamp": datetime.utcnow().isoformat()+"Z"}
    save_json(SAVE_FILE, save)
    print(f"✅ Logged {fishname} in {zone}!")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--zone", required=True, choices=["pond","river","sea"])
    p.add_argument("--location", default="pond")
    p.add_argument("--weather",  default="any", choices=["any","raining","clear"])
    p.add_argument("--override-time",
                   help="YYYY-MM-DD HH:MM (24h) to spoof system time")
    p.add_argument("--catch", help="fish name to mark as caught")
    args = p.parse_args()

    # time
    now = datetime.strptime(args.override_time, "%Y-%m-%d %H:%M") \
          if args.override_time else datetime.now()

    fishdata = load_json(DATA_FILE)
    save     = load_json(SAVE_FILE)

    if args.catch:
        mark_caught(args.zone, args.catch, save)
        return

    avail = list_available(args.zone, now, args.weather, args.location,
                           fishdata, save)
    if not avail:
        print("😔 Nothing's biting right now...")
    else:
        print(f"🎣 Fish available in {args.zone} ({args.location}, {args.weather})")
        for name, caught in avail:
            status = "✅ caught" if caught else "❌ not yet"
            print(f"  • {name:<15} {status}")

if __name__ == "__main__":
    main()
