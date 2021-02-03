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
        if rng >= 0.5:
            should_join = True

    return {"should_join": should_join}


# mechanism
def joins(params, step, sL, s, inputs):
    # print(f'{s=}')
    # print(f'{inputs=}')
    if inputs['should_join']:
        b = broker.Broker()
        s['brokers'][b.id] = b

    key = "joins"
    value = s['brokers']
    return key, value
