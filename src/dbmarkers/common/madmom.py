import csv
from datetime import datetime, timedelta
from typing import Sequence, Dict, Any

Marker = Dict[str, Any]
Markers = Sequence[Marker]

def to_timestamp(dt: datetime, delta: timedelta) -> str:
    return (dt + delta)

def read_downbeat_markers(path: str) -> Markers:
    markers = list()
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    with open(path, newline="") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=("timestamp","beat"), delimiter="\t")
        for row in reader:
            delta = timedelta(seconds=float(row["timestamp"]))
            markers.append(
                {
                    "beat": int(row["beat"]),
                    "timestamp": to_timestamp(now, delta),
                }
            )
    return markers