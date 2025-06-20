import sys, json, argparse
from datetime import datetime
from pathlib import Path

SAVE_PATH = Path("/workspaces/FishELF/save.json")
DATA_PATH = Path("/workspaces/FishELF/fishdata.json")

def load_json(path):
    if not path.exists():
        print(f"[!!] {path} missing")
        sys.exit(1)
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def expand_hour_range(hr):
    if len(hr) == 2 and hr == [0, 23]:
        return list(range(0, 24))  # all hours
    elif len(hr) == 2:
        return list(range(hr[0], hr[1]+1))
    return hr

def is_available(fishmeta, now, weather, location):
    m = now.month
    h = now.hour
    allowed_hours = expand_hour_range(fishmeta["hours"])
    return (
        m in fishmeta["months"] and
        h in allowed_hours and
        (weather in fishmeta["weather"] or "any" in fishmeta["weather"]) and
        location in fishmeta["location"]
    )

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--zone", required=True, choices=["pond", "river", "sea"])
    p.add_argument("--catch", required=True)
    p.add_argument("--weather", default="any", choices=["any", "raining", "clear"])
    p.add_argument("--location", default="normal")
    p.add_argument("--override-time", help="YYYY-MM-DD HH:MM")
    args = p.parse_args()
    now = datetime.strptime(args.override_time, "%Y-%m-%d %H:%M") if args.override_time else datetime.now()

    print(f"[debug] catch: {args.catch}")
    print(f"[debug] zone: {args.zone}")
    print(f"[debug] weather: {args.weather}")
    print(f"[debug] location: {args.location}")
    print(f"[debug] now: {now}")

    data = load_json(DATA_PATH)
    save = load_json(SAVE_PATH)
    fishmeta = data.get(args.zone, {}).get(args.catch)

    if not fishmeta:
        print(f"[!!] Fish '{args.catch}' not found in zone '{args.zone}'")
        return

    for line in fishmeta.get("ascii", []):
        print(line)

    print(f"[debug] fishmeta: {fishmeta}")

    if not is_available(fishmeta, now, args.weather, args.location):
        print("😔 It got away... not available now.")
        return

    caught = save.get(args.zone, {}).get(args.catch, {}).get("caught", False)
    if not caught:
        print("✨ NEW!")
    else:
        print("✅ Already in your Critterpedia.")

    save.setdefault(args.zone, {})[args.catch] = {
        "caught": True,
        "timestamp": now.isoformat() + "Z"
    }
    save_json(SAVE_PATH, save)

if __name__ == "__main__":
    main()
