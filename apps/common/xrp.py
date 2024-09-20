from datetime import datetime
from os import urandom

import xrpl
from cryptoconditions import PreimageSha256
from django.conf import settings
from rest_framework.exceptions import ValidationError
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountObjects
from xrpl.models.transactions import EscrowCreate, EscrowFinish
from xrpl.wallet import Wallet

XRP_LIVE = settings.XRP_LIVE
if XRP_LIVE:
    xrp_url = "https://xrplcluster.com/"
else:
    xrp_url = "https://s.devnet.rippletest.net:51234/"
    # xrp_url = "https://s.altnet.rippletest.net:51234"


def get_account(seed):
    """get_account"""
    client = xrpl.clients.JsonRpcClient(xrp_url)
    if seed == "":
        if XRP_LIVE:
            new_wallet = xrpl.wallet.Wallet.create()
        else:
            new_wallet = xrpl.wallet.generate_faucet_wallet(client)
    else:
        new_wallet = xrpl.wallet.Wallet.from_seed(seed)
    return new_wallet


def get_account_info(accountId):
    """get_account_info"""
    client = xrpl.clients.JsonRpcClient(xrp_url)
    acct_info = xrpl.models.requests.account_info.AccountInfo(
        account=accountId, ledger_index="validated"
    )
    response = client.request(acct_info)
    # return response.result['account_data']
    return response


def get_acc_info(addr):
    client = xrpl.clients.JsonRpcClient(xrp_url)
    return xrpl.account.get_account_root(addr, client)


def send_xrp(seed, amount, destination):
    sending_wallet = xrpl.wallet.Wallet.from_seed(seed)
    client = xrpl.clients.JsonRpcClient(xrp_url)
    payment = xrpl.models.transactions.Payment(
        account=sending_wallet.address,
        amount=xrpl.utils.xrp_to_drops(int(amount)),
        destination=destination,
    )
    try:
        response = xrpl.transaction.submit_and_wait(payment, client, sending_wallet)
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        response = f"Submit failed: {e}"
        raise ValidationError(response)

    return response


def generate_condition():
    randy = urandom(32)
    fulfillment = PreimageSha256(preimage=randy)
    return (
        fulfillment.condition_binary.hex().upper(),
        fulfillment.serialize_binary().hex().upper(),
    )


def add_seconds(numOfSeconds):
    new_date = datetime.now()
    if new_date != "":
        new_date = xrpl.utils.datetime_to_ripple_time(new_date)
        new_date = new_date + int(numOfSeconds)
    return new_date


def create_conditional_escrow(seed, amount, destination, cancel, condition):
    wallet = Wallet.from_seed(seed)
    client = JsonRpcClient(xrp_url)
    cancel_date = add_seconds(cancel)
    source_tag = settings.XRP_SOURCE_TAG

    escrow_tx = EscrowCreate(
        account=wallet.address,
        amount=amount,
        destination=destination,
        finish_after=cancel_date,
        condition=condition,
        source_tag=source_tag,
    )
    # Submit the transaction and report the results
    reply = ""
    try:
        response = xrpl.transaction.submit_and_wait(escrow_tx, client, wallet)
        reply = response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply = f"Submit failed: {e}"
        raise ValidationError(reply)
    return reply


def finish_conditional_escrow(seed, owner, sequence, condition, fulfillment):
    wallet = Wallet.from_seed(seed)
    client = JsonRpcClient(xrp_url)
    finish_tx = EscrowFinish(
        account=wallet.address,
        owner=owner,
        offer_sequence=int(sequence),
        condition=condition,
        fulfillment=fulfillment,
    )
    # Submit the transaction and report the results
    reply = ""
    try:
        response = xrpl.transaction.submit_and_wait(finish_tx, client, wallet)
        reply = response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply = f"Submit failed: {e}"
        raise ValidationError(reply)
    return reply


def get_escrows(account):
    client = JsonRpcClient(xrp_url)
    acct_escrows = AccountObjects(
        account=account, ledger_index="validated", type="escrow"
    )
    response = client.request(acct_escrows)
    return response.result
