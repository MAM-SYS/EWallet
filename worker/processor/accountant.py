import logging
from datetime import datetime
from uuid import UUID

from sqlalchemy import select, insert, desc, update

from dto_pack import TransferStatus
from orm import get_session
from orm.models import Transfer, Transaction, Wallet


async def create_transaction(transfer_number: str, client_id: str, amount: float):
    async with get_session() as session:
        wallet: Wallet = (await session.execute(select(Wallet).where(Wallet.client_id == client_id))).one_or_none()[0]
        await session.execute(insert(Transaction).values(amount=amount, wallet_id=wallet.uuid))
        transaction: Transaction = (await session.execute(select(Transaction)
                                                          .where(Transaction.amount == amount,
                                                                 Transaction.wallet_id == wallet.uuid, )
                                                          .order_by(desc(Transaction.created_at)))).scalars().all()[0]
        await session.execute(update(Transfer)
                              .where(Transfer.number == transfer_number)
                              .values(transaction_id=transaction.uuid,
                                      status=TransferStatus.Succeed.value,
                                      finished_at=datetime.now()))
    await session.commit()


async def fail_transfer(transfer_number: str):
    async with get_session() as session:
        transfer: Transfer = (await session.execute(select(Transfer).where(Transfer.number == transfer_number))).one_or_none()[0]
        transfer.status = TransferStatus.Failed.value
        transfer.finished_at = datetime.now()

    await session.commit()


async def update_schedule_id(transfer_number: str, schedule_id: UUID):
    logging.info("Updating transfer's schedule_id with number %s", transfer_number)
    async with get_session() as session:
        await session.execute(update(Transfer).where(Transfer.number == transfer_number).values(schedule_id=str(schedule_id)))

    await session.commit()


async def cancel_scheduled_transfer(transfer_number: str):
    logging.info("Canceling transfer with number %s", transfer_number)
    async with get_session() as session:
        await session.execute(update(Transfer).where(Transfer.number == transfer_number).values(status=TransferStatus.Canceled.value,
                                                                                                canceled_at=datetime.now()))

    await session.commit()

async def get_wallet_balance(client_id: str):
    logging.info("Fetching client's wallet with id %s", client_id)
    async with get_session() as session:
        wallet: Wallet = (await session.execute(select(Wallet).where(Wallet.client_id == client_id))).one()
        return await wallet[0].balance
