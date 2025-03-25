from collections import defaultdict, Counter
import zoneinfo
from zoneinfo import ZoneInfo
from datetime import datetime, timezone
from itertools import combinations

tz_paths = {
    "2018c": "/Users/dave/workspace/i18n-puzzles/tzcode2018c/stage",
    "2018g": "/Users/dave/workspace/i18n-puzzles/tzcode2018g/stage",
    "2021b": "/Users/dave/workspace/i18n-puzzles/tzcode2021b/stage",
    "2023d": "/Users/dave/workspace/i18n-puzzles/tzcode2023d/stage",
}


def answer(lines: list[str]):
    lines = lines[:-1]

    tz_strings: dict[str, dict[str, set]] = {}
    for line in lines:
        suffix = line.split("; ")[1]
        tz_strings[suffix] = defaultdict(set)

    for db_name, tz_path in tz_paths.items():
        zoneinfo.reset_tzpath([tz_path])
        ZoneInfo.clear_cache()
        for line in lines:
            prefix, tz = line.split("; ")
            dt = datetime.strptime(prefix, "%Y-%m-%d %H:%M:%S")
            dt = dt.replace(tzinfo=ZoneInfo(tz))
            tz_strings[tz][db_name].add(
                dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
            )

    # Now we just need to, for each one, choose an option
    # 4 options for each
    # There is only one possibility?
    # 4^n choices - 262 million for the real input :-(
    # but we can immediately eliminate many choices

    all_timestamps = Counter()
    for tz in tz_strings:
        for zone in tz_paths:
            for ts in tz_strings[tz][zone]:
                all_timestamps[ts] += 1

    for t, v in all_timestamps.items():
        if v >= 4:
            # ensure this timestamp is available in EVERY zone
            for tz in tz_strings:
                for db_name in tz_strings[tz]:
                    if t in tz_strings[tz][db_name]:
                        break
                else:
                    # not found in this tz
                    break
            else:
                # good
                print(t)
