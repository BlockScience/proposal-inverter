import random


def account_global_state_from_delegator_states(params, step, sL, s):
    previous_supply = s['supply']
    previous_reserve = s['reserve']

    # invariant is the value of function V that doesn't change. always S**2/R
    # NOTE: previous_reserve == 0 might be a bad condition?
    invariant = 0
    if previous_reserve > 0:
        invariant = (previous_supply ** 2) / previous_reserve

    # sum the share supply of all delegators
    supply = sum([d.shares() for d in s['delegators'].values()])

    # back out the reserve using the same invariant/function as above.
    reserve = 0
    if invariant > 0:
        reserve = (supply ** 2) / invariant

    # spot price is the derivative at the point of the curve where we are
    spot_price = 0
    if supply > 0:
        spot_price = 2 * reserve / supply

    return {'supply': supply,
            'reserve': reserve,
            'spot_price': spot_price}


def store_supply(params, step, sL, s, inputs):
    key = 'supply'
    value = inputs['supply']
    return key, value


def store_reserve(params, step, sL, s, inputs):
    key = 'reserve'
    value = inputs['reserve']
    return key, value


def store_spot_price(params, step, sL, s, inputs):
    key = 'spot_price'
    value = inputs['spot_price']
    return key, value
