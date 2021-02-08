import random


# policy


def should_leaves(params, step, sL, s):
    # complex, iterate later -- if you would be leaving and not penalized,
    # probability is 1/10.  if there would be a penalty, probability is 1/50
    # each broker has a chance to leave.

    # key=brokerId, value=boolean representing whether the broker should leave
    # print(f'{s=}')

    should_leaves = {}
    funds_to_claim = 0
    for broker_id in s['brokers']:
        b = s['brokers'][broker_id]

        # broker is allowed to leave if they have stayed in longer than
        # min_epochs or unallocated_funds < min_horizon

        if (s['horizon'] < s['min_horizon'] or
           b.time_attached > s['min_epochs']):
            b.allowed_to_leave = True

        if b.stake > 0:
            p = 1/10
        else:
            p = 1/50
        rng = random.random()
        should_leaves[broker_id] = rng < p
        if should_leaves[broker_id]:
            # when a broker leaves, they take their stake and
            # claimable_funds funds with them.
            funds_to_claim += b.stake + b.claimable_funds

    return {'should_leaves': should_leaves, 'funds_to_claim': funds_to_claim}


# mechanism
def leaves(params, step, sL, s, inputs):
    """ When a broker leaves,
    1) member is set to False
    2) they take their stake
    3) they take their claimable_funds

    """
    for should_leave in inputs['should_leaves']:
        if inputs['should_leaves'][should_leave]:
            broker = s['brokers'][should_leave]
            broker.member = False
            broker.holdings += broker.stake
            broker.stake = 0
            broker.holdings += broker.claimable_funds
            broker.claimable_funds = 0

    key = 'leaves'
    value = s['brokers']
    return key, value


def decrement_unallocated_funds_due_to_leaves(params, step, sL, s, inputs):
    """ when a broker leaves,
    1) the unallocated_funds is decreased by the claimable_funds.
        unallocated_funds = s['unallocated_funds']
    """

    key = 'unallocated_funds'
    value = s['unallocated_funds'] - inputs['funds_to_claim']
    return key, value
