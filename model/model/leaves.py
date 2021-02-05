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
    removed_stake = 0
    forfeit_stake = 0
    for broker_id in s['brokers']:
        b = s['brokers'][broker_id]
        if b.stake > 0:
            p = 1/10
        else:
            p = 1/50
        rng = random.random()
        should_leaves[broker_id] = rng < p
        if should_leaves[broker_id]:
            # when a broker leaves, they take their
            # claimable_funds funds with them.
            funds_to_claim += b.claimable_funds
            if b.leaver_status:
                forfeit_stake += b.stake
            else:
                removed_stake += b.stake
                b.holdings += b.stake

    return {
        'should_leaves': should_leaves,
        'funds_to_claim': funds_to_claim, 
        'removed_stake': removed_stake, 
        'forfeit_stake':forfeit_stake }


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
            broker.stake = 0
            broker.holdings += broker.claimable_funds
            broker.claimable_funds = 0
            if broker.leaver_status:
                broker.holdings += broker.stake


    key = 'leaves'
    value = s['brokers']
    return key, value


def decrement_allocated_funds_due_to_leaves(params, step, sL, s, inputs):
    """ when a broker leaves,
    1) the allocated_funds is decreased by the claimable_funds.
        allocated_funds = s['allocated_funds']
    """

    key = 'allocated_funds'
    value = s['allocated_funds'] - inputs['funds_to_claim']
    return key, value

def decrement_total_stake_due_to_leaves(params, step, sL, s, inputs):
    """ when a broker leaves,

    """

    key = "total_broker_stake"
    value = s["total_broker_stake"] - inputs['removed_stake'] - inputs['forfeit_stake']
    return key, value

def increment_unallocated_funds_due_to_forfeit_stake(params, step, sL, s, inputs):
    """ when a broker leaves,

    """

    key = "unallocated_funds"
    value = s["unallocated_funds"] +  inputs['forfeit_stake']
    return key, value