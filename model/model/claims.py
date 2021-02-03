import random

CLAIM_CONST = 25


def should_make_claims(params, step, sL, s):
    """
    each broker with a_i > 0 makes a claim if: rng > CLAIM_CONST / a_i
    """
    # key broker_id, value bool whether to make a claim
    should_make_claims = {}

    # does each broker make a claim?
    for broker_id, broker in s['brokers'].items():
        if broker.claimable_funds > 0:
            rng = random.random()
            should_make_claim = rng > CLAIM_CONST / broker.claimable_funds
            should_make_claims[broker_id] = should_make_claim
    print(f'{should_make_claims=}')
    return {'should_make_claims': should_make_claims}


def make_claims(params, step, sL, s, inputs):
    should_make_claims = inputs['should_make_claims']
    # apply each claim

    for broker_id, should_make_claim in should_make_claims.items():
        if should_make_claim:
            s['brokers'][broker_id].holdings += \
                 s['brokers'][broker_id].claimable_funds
            s['brokers'][broker_id].claimable_funds = 0
    key = "make_claims"
    value = s['brokers']
    return key, value
