import logging
from asyncio import Lock
from decimal import Decimal
from http import HTTPStatus

import aiohttp
from processor.accountant import create_transaction, fail_transfer, get_wallet_balance

lock = Lock()

async def do_deposit_transfer(transfer_number: str, client_id: str, amount: float):
    logging.info("Interacting with third party service...")
    balance: Decimal = await get_wallet_balance(client_id)

    async with lock:
        if amount <= balance:
            async with aiohttp.ClientSession() as session:
                async with session.post('http://localhost:8010/') as resp:
                    if resp.status == HTTPStatus.OK:
                        await create_transaction(transfer_number, client_id, amount)
                    elif resp.status == HTTPStatus.SERVICE_UNAVAILABLE:
                        await fail_transfer(transfer_number)
        else:
            await fail_transfer(transfer_number)