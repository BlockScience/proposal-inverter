def allocated_funds(params, step, sL, s, inputs):    
    value = s['allocated_funds'] + params['allocation_per_epoch']
    key = 'allocated_funds'
    return (key, value)

def unallocated_funds(params, step, sL, s, inputs):    
    value = s['allocated_funds'] - params['allocation_per_epoch']
    key = 'allocated_funds'
    return (key, value)

def allocate_funds_to_member_brokers(params, step, sL, s, inputs):
    amount_allocated = params['allocation_per_epoch'] / s['num_member_brokers']

    for broker in s['brokers']:
        if broker.member:
            broker.holdings += amount_allocated 

    value = s['brokers']
    key = 'brokers'
    return (key, value)


