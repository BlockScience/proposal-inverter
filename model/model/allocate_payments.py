# policies:
# no inputs, because the outputs here are the inputs
def check_brokers(params, step, sL, s):
    # print(f'4: {params=}')
    # True if the number of member brokers is
    # greater than or equal to the minimum number of brokers.
    value = s['num_member_brokers'] >= params['min_brokers']
    key = 'check_brokers'
    return {key: value}


# mechanisms:
def allocated_funds(params, step, sL, s, inputs):
    # print(f'1: {params=}')
    value = s['allocated_funds']
    # if there are enough brokers, put the allocation in the brokers' hands.
    if inputs['check_brokers']:
        value += params['allocation_per_epoch']

    key = 'allocated_funds'
    return key, value


def unallocated_funds(params, step, sL, s, inputs):
    # print(f'2: {params=}')
    value = s['unallocated_funds']
    if inputs['check_brokers']:
        value -= params['allocation_per_epoch']

    key = 'unallocated_funds'
    return key, value


def allocate_funds_to_member_brokers(params, step, sL, s, inputs):
    # print(f'3: {params=}')
    if inputs['check_brokers']:
        amount_allocated = (params['allocation_per_epoch'] /
                            s['num_member_brokers'])

        for broker in s['brokers'].values():
            if broker.member:
                broker.claimable_funds += amount_allocated

    value = s['brokers']
    key = 'brokers'
    return key, value


def total_broker_stake(params, step, sL, s, inputs):
    total_broker_stake = 0
    for broker in s['brokers'].values():
        if broker.member:
            total_broker_stake += broker.stake

    value = total_broker_stake
    key = 'total_broker_stake'
    return key, value
