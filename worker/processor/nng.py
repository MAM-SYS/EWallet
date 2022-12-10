import json
import logging
from importlib import import_module

import pynng
from pynng import Message

from constants import NNG_INTERNAL_ADDRESS
from processor.decorators import callbacks


async def event_handler():
    logging.info("Listening for event...")

    import_module('processor.event_callbacks')
    with pynng.Sub0() as sock:
        sock.subscribe('transfer')
        sock.dial(NNG_INTERNAL_ADDRESS, block=False)

        while True:

            try:
                message: Message = await sock.arecv_msg()
                logging.info("Incoming message: %s", message.bytes)

                transition, *json_data = message.bytes.decode("utf-8").split(':', 1)
                if data := json.loads(json_data[0]):
                    await callbacks[data['transition']](**data)
            except Exception as e:
                logging.error(f"Exception while processing the message because of %s", e)
                continue
