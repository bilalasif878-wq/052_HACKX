from collections import defaultdict
import json
import os

RAPID_SWITCH_THRESHOLD_SEC = 15
IGNORE_DOMAINS = {"", "newtab", "chrome"}


def process_session(session):
    events = session.get("events", [])
    started_at = session.get("startedAt")
    ended_at = session.get("endedAt")

    if not events or not started_at or not ended_at:
        raise ValueError("Invalid session data")

    duration_sec = round((ended_at - started_at) / 1000)

    # Sort events chronologically
    events = sorted(events, key=lambda e: e["ts"])

    tab_switches = 0
    rapid_switches = 0

    domain_time = defaultdict(int)

    last_ts = started_at
    active_domain = None

    for e in events:
        current_ts = e["ts"]
        delta_sec = max(0, int((current_ts - last_ts) / 1000))

        # Assign time to last active domain
        if active_domain and active_domain not in IGNORE_DOMAINS:
            domain_time[active_domain] += delta_sec

        # Detect rapid switching
        if e["event"] == "activated":
            tab_switches += 1
            if delta_sec < RAPID_SWITCH_THRESHOLD_SEC:
                rapid_switches += 1

        # Update active domain when a real page loads
        if e["event"] == "updated":
            domain = e.get("domain")
            if domain and domain not in IGNORE_DOMAINS:
                active_domain = domain

        last_ts = current_ts

    # Assign remaining time until session end
    if active_domain and active_domain not in IGNORE_DOMAINS:
        domain_time[active_domain] += int((ended_at - last_ts) / 1000)

    switch_rate_per_min = round((tab_switches / max(duration_sec, 1)) * 60, 2)

    top_domains = sorted(
        domain_time.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return {
        "durationSec": duration_sec,
        "totalEvents": len(events),
        "tabSwitches": tab_switches,
        "switchRatePerMin": switch_rate_per_min,
        "uniqueDomains": len(domain_time),
        "topDomains": [
            {"domain": d, "estimatedTimeSec": t}
            for d, t in top_domains
        ],
        "rapidSwitches": rapid_switches
    }


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SAMPLE_PATH = os.path.join(BASE_DIR, "sample_session.json")

    with open(SAMPLE_PATH, "r") as f:
        session = json.load(f)

    metrics = process_session(session)
    print(json.dumps(metrics, indent=2))