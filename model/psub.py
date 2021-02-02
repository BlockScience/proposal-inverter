# from .behavior import update_a
from .model import broker
from .model.allocate_payments import *
from .model.leaves import *

# random numbers in policies (stored in input for variables), deterministic in variables
## "input" should be called "policy_output"




psubs = [
    {   "label": "Payments",
        "policies": {},
        "variables": {},
        # random variable, flip a coin 0-10
    },
    {   "label": "Allocate Payments",
        "policies": {},
        "variables": {
            "allocated_funds": allocated_funds,     # A
            "unallocated_funds": unallocated_funds,   # R
            # "total_funds": broker.deploy_agreement,         # F
            # "committed_brokers": ?,   # B
            "brokers": allocate_funds_to_member_brokers,   #each broker gets a share of allocated funds
            # "total_broker_stake": ?,  # S
            # "horizon": ?,             # H    
        }
    },
    {   "label": "Claims",
        "policies": {},
        "variables": {},
    },
    {
        "label": "Leaves", #complex, iterate later -- if you would be leaving and not penalized, probability is 1/10.  if there would be a penalty, probability is 1/50
        "policies": {},
        "variables": {
                "num_member_brokers": count_members,
        }

    },
    {   "label": "Joins", #if there's a vacant spot, flip a coin (heads, they join, tails nobody joins)
        "policies": {},
        "variables": {},
    },
]