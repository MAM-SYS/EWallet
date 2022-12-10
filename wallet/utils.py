from datetime import datetime
from typing import Optional, Callable, Dict, Tuple

import pytz

from dto_pack import TransferStatus

transition_callbacks: Dict[Tuple[str, TransferStatus], Callable[[str], None]] = {}


def get_current_time(time_zone=pytz.utc):
    return time_zone.fromutc(datetime.now())


def register_transition_callback(enter_trigger: Optional[TransferStatus] = None,
                                 exit_trigger: Optional[TransferStatus] = None):
    def decorate(func: Callable[[str], None]):
        if enter_trigger:
            transition_callbacks['enter', enter_trigger] = func
        elif exit_trigger:
            transition_callbacks['exit', exit_trigger] = func

        return func

    return decorate
