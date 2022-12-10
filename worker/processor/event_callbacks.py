import logging
from datetime import datetime, timedelta
from uuid import UUID

from aioscheduler.task import Task

from dto_pack import TransferTransitionTrigger
from processor.accountant import update_schedule_id, cancel_scheduled_transfer
from processor.decorators import register_event_handler
from processor.logic import do_deposit_transfer
from processor.scheduler import manager, scheduled_tasks


@register_event_handler(TransferTransitionTrigger.Submit)
async def schedule_deposit_transfer(transfer_number: str, client_id: str, amount: float, scheduled_at: float, *args, **kwargs):
    logging.info("Scheduling deposit transfer with number %s", transfer_number)
    task: Task = manager.schedule(do_deposit_transfer(transfer_number, client_id, amount),
                                  datetime.fromisoformat(scheduled_at).replace(tzinfo=None) - timedelta(hours=3, minutes=30))

    await update_schedule_id(transfer_number, task.uuid)
    scheduled_tasks[task.uuid] = task


@register_event_handler(TransferTransitionTrigger.Cancel)
async def cancel_scheduled_deposit_transfer(transfer_number: str, schedule_id: str, *args, **kwargs):
    scheduled_tasks.pop(UUID(schedule_id))
    await cancel_scheduled_transfer(transfer_number)
