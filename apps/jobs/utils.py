import logging

from rest_framework import serializers
from xrpl.utils import xrp_to_drops

from apps.common.exchange import currency_conversion
from apps.common.models import Currency
from apps.common.xrp import (
    create_conditional_escrow,
    finish_conditional_escrow,
    generate_condition,
    get_acc_info,
)


def create_escrow(job, freelancer):
    if job.escrow_sequence and job.escrow_condition and job.escrow_fulfillment:
        raise serializers.ValidationError({"message": "Escrow already created"})

    company = job.company
    if not company:
        raise serializers.ValidationError({"message": "No company associated with job"})

    # check if company has xrp address and seed
    if not company.xrp_address and not company.xrp_seed:
        raise serializers.ValidationError({"message": "Update xrp address and seed"})

    # check currency
    currency = job.currency
    if currency != Currency.USD:
        raise serializers.ValidationError({"message": "Price should be in USD"})

    # convert usd to xrp
    xrp_price = currency_conversion(job.price, currency=Currency.XRP)

    # check sufficient balance
    address = company.xrp_address
    price = xrp_price
    reserve = 15  # ripple accounts must have reserve balance
    price_n_reserve = price + reserve
    price_n_reserve_in_drops = int(xrp_to_drops(price_n_reserve))

    res = get_acc_info(address)
    acc_bal = int(res["Balance"])
    if price_n_reserve_in_drops > acc_bal:
        raise serializers.ValidationError(
            {"message": "Insufficient Balance to create job"}
        )

    # Create escrow for Job
    condition, fulfillment = generate_condition()
    company_seed = company.xrp_seed
    freelancer_address = freelancer.xrp_address

    if not freelancer_address:
        raise serializers.ValidationError(
            {"message": "Freelancer xrp address required"}
        )

    finish_time = 60  # In seconds
    price_in_drops = xrp_to_drops(price)
    try:
        escrow = create_conditional_escrow(
            company_seed,
            price_in_drops,
            freelancer_address,
            finish_time,
            condition,
        )
    except Exception as e:
        logging.warning(e)
        raise serializers.ValidationError(
            {"message": "Escrow creation failed", "error": e}
        )
    # Update jobs
    escrow_sequence = escrow["tx_json"]["Sequence"]
    job.escrow_condition = condition
    job.escrow_fulfillment = fulfillment
    job.escrow_sequence = escrow_sequence
    job.escrow_status = job.EscrowStatus.CREATED
    job.save(
        update_fields=[
            "escrow_sequence",
            "escrow_condition",
            "escrow_fulfillment",
            "escrow_status",
            "updated_at",
        ]
    )
    return {"message": "Escrow created"}


def redeem_escrow(job):
    sequence = job.escrow_sequence
    condition = job.escrow_condition
    fulfillment = job.escrow_fulfillment
    if not sequence or not condition or not fulfillment:
        raise serializers.ValidationError({"message": "Escrow not created"})

    # redeem escrow for Job
    company = job.company
    company_seed = company.xrp_seed
    company_address = company.xrp_address
    try:
        finish_conditional_escrow(
            company_seed, company_address, sequence, condition, fulfillment
        )
    except Exception as e:
        logging.warning(e)
        raise serializers.ValidationError(
            {"message": "Failed to redeem escrow", "error": e}
        )

    # update job escrow status
    job.escrow_status = job.EscrowStatus.REDEEMED
    job.save(update_fields=["escrow_status", "updated_at"])

    return {"message": "Escrow redeemed"}
