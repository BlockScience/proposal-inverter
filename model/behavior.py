import numpy as np
def payment_rng(params, step, prev_state, state):
    
    amt = 2*np.random.rand()*params["allocation_per_epoch"]

    return {'amt':amt}