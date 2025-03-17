from pytz import timezone
from datetime import datetime

if __name__ == "__main__":
    f = open("input4.txt", 'r')
    lines = f.read().split('\n')

    total = 0
    while lines:
        first_line = lines.pop(0)
        second_line = lines.pop(0)

        first_tz = first_line[11:].split(' ')[0]
        second_tz = second_line[11:].split(' ')[0]

        first_timestamp = first_line[11:].split(first_tz)[1].lstrip()
        second_timestamp = second_line[11:].split(second_tz)[1].lstrip()
        lines.pop(0)

        source_ts = timezone(first_tz).localize(datetime.strptime(first_timestamp, '%b %d, %Y, %H:%M'))
        dest_ts = timezone(second_tz).localize(datetime.strptime(second_timestamp, '%b %d, %Y, %H:%M'))

        delta = (int(dest_ts.timestamp() - source_ts.timestamp()) // 60)
        total += delta
        print(delta)

    print(total)
