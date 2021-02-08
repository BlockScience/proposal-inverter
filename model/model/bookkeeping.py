def update_time_attached(params, step, sL, s, inputs):

    for broker in s['brokers'].values():
        if broker.member:
            broker.time_attached += 1

    key = 'brokers'
    value = s['brokers']

    return key, value


def total_broker_stake(params, step, sL, s, inputs):
    total_broker_stake = sum([b.stake for b in s['brokers'].values()])

    key = 'total_broker_stake'
    value = total_broker_stake

    return key, value
