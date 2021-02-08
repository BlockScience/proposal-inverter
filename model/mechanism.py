""" this file is for general state changes and bookkeeping """


def payment_to_unallocated(params, step, sL, s, inputs):

    key = 'unallocated_funds'
    value = s['unallocated_funds'] + inputs['payment_amt']

    return key, value


def update_time_attached(params, step, sL, s, inputs):

    for broker in s['brokers'].values():
        if broker.member:
            broker.time_attached += 1

    key = 'brokers'
    value = s['brokers']

    return key, value
