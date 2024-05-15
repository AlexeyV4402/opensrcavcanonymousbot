from yoomoney import Client, Quickpay
from datetime import datetime, timedelta, date
from asyncio import sleep
from config import YOOMONEY

from json import load, dump

import database

client = Client(YOOMONEY["token"])

user = client.account_info()

unactive_payments = []


def create_quickpay(user_id, label, price):
    quickpay = Quickpay(
        receiver=str(YOOMONEY["owner_wallet_id"]),
        quickpay_form="shop",
        targets="Payment",
        paymentType="SB",
        sum=price,
        label=f"{str(user_id)}|{label}"
        )
    return {
        "base_url": quickpay.base_url,
        "redirected_url": quickpay.redirected_url
    }


async def check_to_payment(user_id, time: timedelta, label: str):
    history = client.operation_history(label=str(user_id)+"|"+label)
    for operation in history.operations:
        if operation.status == "success":
            if operation.operation_id not in unactive_payments:
                if datetime.now() - time <= operation.datetime:
                    await unactivate_payments(operation.operation_id)
                    return True
    return False


async def unactivate_payments(operation_id):
    unactive_payments.append(operation_id)
    await sleep(45 * 60)
    unactive_payments.remove(operation_id)
