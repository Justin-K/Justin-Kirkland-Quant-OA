from datetime import datetime, timezone
from dateutil import tz
'''
Title: Conversion Between Two Time Zones In Python
Author: Obersteiner, Florian
Date: 25 June 2021
Type: Source Code
Available at: www.stackoverflow.com/a/68135024
Description: The function cited (from_utc_timestamp_to_local_datetime()) was inspired by Obersteiner's code.
'''


def from_utc_timestamp_to_local_datetime(utc_timestamp: int) -> datetime:
    local_tz = datetime.now(timezone.utc).astimezone().tzinfo
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(local_tz.__str__())
    utc = datetime.utcfromtimestamp(utc_timestamp/1000)
    utc = utc.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)
