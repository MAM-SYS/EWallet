from ast import literal_eval
from typing import Dict, Any

config: Dict[str, Any] = {}


def parse_config(val: str) -> Any:
    try:
        return literal_eval(val)
    except:
        return val
