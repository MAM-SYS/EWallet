from typing import Callable, Dict, Tuple, Any

from dto_pack import TransferTransitionTrigger

callbacks: Dict[TransferTransitionTrigger, Callable[[Dict[str, Any]], None]] = {}


def register_event_handler(transition_trigger: TransferTransitionTrigger):
    def decorate(func: Callable[[Dict[str, Any]], None]):
        callbacks[transition_trigger] = func
        return func

    return decorate
