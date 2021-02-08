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

    # update epoch counter for current members
    # print(s['brokers'])
    for b in s['brokers'].values():
        if b.member:
            b.iterate_epoch_counter

    # add new members
    if inputs['should_join']:
        b = broker.Broker()
        s['brokers'][b.id] = b

    key = "brokers"
    value = s['brokers']
    return key, value


def increment_total_stake(params, step, sL, s, inputs):

    key = int(inputs['should_join'])*params["required_stake"]
    value = s['total_broker_stake']

    return key, value
