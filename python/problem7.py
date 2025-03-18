from typing import List
from datetime import datetime, timedelta
import pytz

def answer(lines: List[str]):
    gmt = pytz.timezone('GMT')
    tz1 = pytz.timezone('America/Halifax')
    tz2 = pytz.timezone('America/Santiago')

    total = 0
    for i, line in enumerate(lines):
        if not line:
            continue

        dt_str, correct_minutes_str, incorrect_minutes_str = line.split('\t')
        correct_minutes = int(correct_minutes_str)
        incorrect_minutes = int(incorrect_minutes_str)
        dt = datetime.strptime(dt_str.rsplit('.000', 1)[0], '%Y-%m-%dT%H:%M:%S')
        offset_str = dt_str.rsplit('.000', 1)[1]
        if offset_str == "-04:00":
            hours_offset = 4
        elif offset_str == "-03:00":
            hours_offset = 3

        dt += timedelta(hours=hours_offset)
        dt = gmt.localize(dt.replace(tzinfo=None))

        valid_tzs = []
        for tz in [tz1, tz2]:
            normalized_dt = tz.normalize(dt)
            prefix = normalized_dt.strftime("%Y-%m-%dT%H:%M:%S")
            if dt_str.startswith(prefix):
                valid_tzs.append(tz)

        if not valid_tzs:
            raise Exception("Did not find valid tz")

        # dt is now GMT, so we can correct the minutes now
        corrected_dt = dt - timedelta(minutes=incorrect_minutes) + timedelta(minutes=correct_minutes)
        localized_correct_dt = valid_tzs[0].normalize(corrected_dt)
        print(localized_correct_dt.strftime('%Y-%m-%dT%H:%M:%S.000%z'))

        total += (localized_correct_dt.hour * (i + 1))
    print(total)
