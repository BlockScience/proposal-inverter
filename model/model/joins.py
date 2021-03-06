from . import broker
import random
from . import helper_functions


# policy
def should_join(params, step, sL, s):
    # flip a coin (1 joins if there's room and random says to)
    should_join = False
    is_spot_open = (params['max_brokers'] >
                    helper_functions.count_members(s['brokers']))

    if is_spot_open:
        rng = random.random()
        horizon = s["unallocated_funds"]/params["allocation_per_epoch"]
        if rng >= 1/horizon:
            should_join = True

    return {"should_join": should_join}


# mechanism
def joins(params, step, sL, s, inputs):
    # add new members
    if inputs['should_join']:
        b = broker.Broker()
        s['brokers'][b.id] = b

    key = "brokers"
    value = s['brokers']
    return key, value
