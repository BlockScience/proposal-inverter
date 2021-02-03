# policies:
# no inputs, because the outputs here are the inputs
def check_brokers(params, step, sL, s):
    # print(f'4: {params=}')
    value = s['num_member_brokers'] >= params['min_brokers']
    key = 'check_brokers'
    return {key: value}


# mechanisms:
def allocated_funds(params, step, sL, s, inputs):
    # print(f'1: {params=}')
    value = s['allocated_funds']
    if inputs['check_brokers']:
        value += params['allocation_per_epoch']

    key = 'allocated_funds'
    return key, value


def unallocated_funds(params, step, sL, s, inputs):
    # print(f'2: {params=}')
    value = s['allocated_funds']
    if inputs['check_brokers']:
        value -= params['allocation_per_epoch']

    key = 'allocated_funds'
    return key, value


def allocate_funds_to_member_brokers(params, step, sL, s, inputs):
    # print(f'3: {params=}')
    if inputs['check_brokers']:
        amount_allocated = (params['allocation_per_epoch'] /
                            s['num_member_brokers'])

        for broker in s['brokers']:
            if broker.member:
                broker.holdings += amount_allocated

    value = s['brokers']
    key = 'brokers'
    return key, value
