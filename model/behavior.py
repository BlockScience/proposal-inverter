""" this file is for general policies """
import scipy.stats as stats


def payment_amt(params, step, prev_state, state):

    # behavior model where payers only pay to ensure brokers cannot leave early
    horizon = state["unallocated_funds"]/params["allocation_per_epoch"]

    amt = 0

    if horizon < 2*params["min_horizon"]:
        amt = .5*params["allocation_per_epoch"]*stats.expon.rvs()
    
    # if horizon < params["min_horizon"]:
    #     amt += params["allocation_per_epoch"] 

    return {'payment_amt': amt}
