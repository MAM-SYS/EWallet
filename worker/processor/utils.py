import struct
import uuid
from datetime import datetime


def uuid_comb() -> uuid.UUID:
    uuid_array = bytearray(uuid.uuid1().bytes)
    base_date = datetime(1900, 1, 1)
    now = datetime.now()
    days = now - base_date
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    sec = int((datetime.now() - midnight).total_seconds() * 300)

    days_array = struct.pack('I', days.days)
    sec_array = struct.pack('L', sec)

    uuid_array[-6:-4] = days_array[:2:][::-1]
    uuid_array[-4:] = sec_array[:4:][::-1]

    return uuid.UUID(bytes=bytes(uuid_array))
