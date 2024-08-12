from datetime import datetime
from os import urandom

import xrpl
from cryptoconditions import PreimageSha256
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountObjects
from xrpl.models.transactions import EscrowCreate, EscrowFinish
from xrpl.wallet import Wallet

testnet_url = "https://s.devnet.rippletest.net:51234/"
# testnet_url = "https://s.altnet.rippletest.net:51234"
mainnet_url = "https://xrplcluster.com/"


def get_account(seed):
    """get_account"""
    client = xrpl.clients.JsonRpcClient(testnet_url)
    if seed == "":
        new_wallet = xrpl.wallet.generate_faucet_wallet(client)
    else:
        new_wallet = xrpl.wallet.Wallet.from_seed(seed)
    return new_wallet


def get_account_info(accountId):
    """get_account_info"""
    client = xrpl.clients.JsonRpcClient(testnet_url)
    acct_info = xrpl.models.requests.account_info.AccountInfo(
        account=accountId, ledger_index="validated"
    )
    response = client.request(acct_info)
    # return response.result['account_data']
    return response


def send_xrp(seed, amount, destination):
    sending_wallet = xrpl.wallet.Wallet.from_seed(seed)
    client = xrpl.clients.JsonRpcClient(testnet_url)
    payment = xrpl.models.transactions.Payment(
        account=sending_wallet.address,
        amount=xrpl.utils.xrp_to_drops(int(amount)),
        destination=destination,
    )
    try:
        response = xrpl.transaction.submit_and_wait(payment, client, sending_wallet)
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        response = f"Submit failed: {e}"

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
    client = JsonRpcClient(testnet_url)
    cancel_date = add_seconds(cancel)

    escrow_tx = EscrowCreate(
        account=wallet.address,
        amount=amount,
        destination=destination,
        cancel_after=cancel_date,
        condition=condition,
    )
    # Submit the transaction and report the results
    reply = ""
    try:
        response = xrpl.transaction.submit_and_wait(escrow_tx, client, wallet)
        reply = response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply = f"Submit failed: {e}"
    return reply


def finish_conditional_escrow(seed, owner, sequence, condition, fulfillment):
    wallet = Wallet.from_seed(seed)
    client = JsonRpcClient(testnet_url)
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
    return reply


def get_escrows(account):
    client = JsonRpcClient(testnet_url)
    acct_escrows = AccountObjects(
        account=account, ledger_index="validated", type="escrow"
    )
    response = client.request(acct_escrows)
    return response.result
