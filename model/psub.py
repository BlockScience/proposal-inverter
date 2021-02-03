# from .behavior import update_a
from .model.allocate_payments import (allocated_funds, unallocated_funds,
                                      check_brokers,
                                      allocate_funds_to_member_brokers)
from .model.leaves import should_leaves, leaves
from .model.joins import should_join, joins
from .model.helper_functions import count_brokers

from .mechanism import payment_to_unallocated
from .behavior import payment_rng

psubs = [
    {
        "label": "Payments",
        "policies": {'rng':payment_rng},
        "variables": {
                        'unallocated_funds': payment_to_unallocated},
        #                'total_funds': payment_to_total
        # random variable, flip a coin 0-10
    },
    {
        "label": "Allocate Payments",
        "policies": {
            "check_brokers": check_brokers
        },
        "variables": {
            "allocated_funds": allocated_funds,     # A
            "unallocated_funds": unallocated_funds,   # R
            # "total_funds": broker.deploy_agreement,         # F
            # "committed_brokers": committed_brokers,   # B
            # each broker gets a share of allocated funds
            "brokers": allocate_funds_to_member_brokers,
            # "total_broker_stake": ?,  # S
            # "horizon": ?,             # H
        }
    },
    {
        "label": "Claims",
        "policies": {},
        "variables": {},
    },
    {
        "label": "Leaves",
        "policies": {
            "should_leaves": should_leaves
            },
        "variables": {
            "brokers": leaves,
            "num_member_brokers": count_brokers
            # "num_member_brokers": count_members,
            }
    },
    {
        # if there's a vacant spot, flip a coin
        # (heads, they join, tails nobody joins)
        "label": "Joins",
        "policies": {
            "should_join": should_join
            },
        "variables": {
            "brokers": joins,
            "num_member_brokers": count_brokers
            },
    },
]
