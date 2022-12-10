import asyncio
import logging.config
import os

import uvloop
from dotenv import load_dotenv

import orm
import settings
from constants import ConfigKeys
from processor.nng import event_handler
from settings import config, parse_config
from processor.scheduler import init_scheduler
dotenv_config = load_dotenv()
loop = uvloop.new_event_loop()


async def bootstrap():
    asyncio.create_task(init_scheduler())
    asyncio.create_task(event_handler())


if __name__ == '__main__':
    asyncio.set_event_loop(loop)
    config.update({key: parse_config(os.getenv(key)) for key in os.environ})
    logging.config.fileConfig(settings.config[ConfigKeys.LoggingConfig])
    orm.initialize()
    loop.run_until_complete(bootstrap())
    loop.run_forever()
