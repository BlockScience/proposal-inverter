def count_members(params, step, sL, s, inputs):    
    value = sum(1 for broker in s['brokers'] if broker.member)
    return value
