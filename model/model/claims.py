
import random
CLAIM_CONST = 10


def should_make_claims(params, step, sL, s):
    """
    each broker with a_i > 0 makes a claim if: rng > CLAIM_CONST / a_i
    """
    # key broker_id, value bool whether to make a claim
    should_make_claims = {}
    funds_to_claim = 0
    # does each broker make a claim?
    for broker_id, broker in s['brokers'].items():
        if broker.claimable_funds > 0:
            rng = random.random()
            should_make_claim = rng > CLAIM_CONST / broker.claimable_funds
            should_make_claims[broker_id] = should_make_claim
            if should_make_claim:
                funds_to_claim += broker.claimable_funds
    #print(f'{should_make_claims=}')
    return {'should_make_claims': should_make_claims,
            'funds_to_claim': funds_to_claim}


def make_claims(params, step, sL, s, inputs):
    """ increase holdings for each broker making a claim by the
    amount of their claimable_funds
    """

    should_make_claims = inputs['should_make_claims']
    # apply each claim

    for broker_id, should_make_claim in should_make_claims.items():
        if should_make_claim:
            s['brokers'][broker_id].holdings += \
                 s['brokers'][broker_id].claimable_funds
            s['brokers'][broker_id].claimable_funds = 0

    key = 'make_claims'
    value = s['brokers']
    return key, value


def decrement_allocated_funds_by_claims(params, step, sL, s, inputs):
    """ decrease unallocated_funds for each broker making a claim by the
    amount of their claimable_funds
    """

    allocated_funds = s['unallocated_funds'] - inputs['funds_to_claim']

    key = 'allocated_funds'
    value = allocated_funds
    return key, value
