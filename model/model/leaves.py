import random


# policy


def should_leaves(params, step, sL, s):
    # complex, iterate later -- if you would be leaving and not penalized,
    # probability is 1/10.  if there would be a penalty, probability is 1/50
    # each broker has a chance to leave.

    # key=brokerId, value=boolean representing whether the broker should leave
    # print(f'{s=}')
    should_leaves = {}
    for broker_id in s['brokers']:
        b = s['brokers'][broker_id]
        if b.stake > 0:
            p = 1/10
        else:
            p = 1/50
        rng = random.random()
        should_leaves[broker_id] = rng < p

    return {"should_leaves": should_leaves}


# mechanism
def leaves(params, step, sL, s, inputs):
    # should_leave is a broker Id
    # so we can use it to access the broker in s['brokers'].
    # print(f'{inputs=}')
    for should_leave in inputs['should_leaves']:
        if inputs['should_leaves'][should_leave]:
            s['brokers'][should_leave].member = False

    key = "leaves"
    value = s['brokers']
    return key, value
