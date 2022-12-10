import logging
from typing import Dict
from uuid import UUID

from aioscheduler import Manager
from aioscheduler.task import Task

manager: Manager
scheduled_tasks: Dict[UUID, Task] = {}


async def init_scheduler():
    global manager

    logging.info("Initializing scheduler...")
    manager = Manager(100)
    manager.start()
