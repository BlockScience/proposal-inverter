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
    for broker_id, b in s['brokers'].items():
        if b.allowed_to_leave:
            p = 1/10
        else:
            p = 1/50

        rng = random.random()
        should_leaves[broker_id] = rng < p
        if should_leaves[broker_id]:
            # when a broker leaves, they take their
            # claimable_funds funds with them.
            funds_to_claim += b.claimable_funds
            if b.allowed_to_leave:
                removed_stake += b.stake
            else:
                forfeit_stake += b.stake

    return {
        'should_leaves': should_leaves,
        'funds_to_claim': funds_to_claim,
        'removed_stake': removed_stake,
        'forfeit_stake': forfeit_stake
        }


# mechanism

# broker is allowed to leave if they have stayed in longer than
# min_epochs or unallocated_funds < min_horizon
def allowed_to_leave(params, step, sL, s, inputs):
    # 1) first check the horizon (if the horizon is too short all brokers can leave)
    # 2) if the horizon is not too short then only brokers who have been members
    # longer than the min period can leave

    # calculate the horizon
    # print(f'')
    horizon = s['unallocated_funds'] / params['allocation_per_epoch']
    brokers = s['brokers']

    if len(brokers) > 0:
        for b in brokers.values():
            if horizon < params['min_horizon'] or b.time_attached >= params['min_epochs']:
                b.allowed_to_leave = True
    
    key = 'brokers'
    value = brokers
    return key, value


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
            if broker.allowed_to_leave:
                broker.holdings += broker.stake

    key = 'brokers'
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


def increment_unallocated_funds_due_to_forfeit_stake(params, step, sL, s, inputs):
    """ when a broker leaves,
    3) the unallocated_funds is increased by the forfeit_stake
    """

    key = "unallocated_funds"
    value = s["unallocated_funds"] + inputs['forfeit_stake']
    return key, value
