import numpy as np


def payment_amt(params, step, prev_state, state):
    amt = 2*np.random.rand()*params["allocation_per_epoch"]
    return {'payment_amt': amt}
