
import scipy.stats as stats

#NOTE: returns the broker that owns the delegation contract
#TODO: will eventually take some arguments like the delegation contract id
def get_owner():
    return 1

def revenue_amt(params, step, prev_state, state):
    #revenue_amt = params["expected_revenue"] * stats.expon.rvs()
    print (state['brokers'].keys())
    if get_owner() in state['brokers']:
        revenue_amt = state['brokers'][get_owner()].holdings #or should this be claimable_funds?
    else:
        revenue_amt = 0
    print(revenue_amt)
    # print(f'{revenue_amt=}')
    return {'revenue_amt': revenue_amt}

def store_revenue(params, step, sL, s, inputs):
    # print('storing revenue')
    key = 'period_revenue'
    value = inputs['revenue_amt']

    return key, value

#TODO: decrease broker holdings when distributed
def distribute_revenue(params, step, sL, s, inputs):
    revenue = s['period_revenue']
    owners_share = params['owners_share']
    supply = s['supply']

    # step 1: collect revenue from the state
    non_owners_share = ((1-owners_share) * revenue)
    revenue_per_share = non_owners_share / supply

    for id, delegator in s['delegators'].items():
        if id == 0:
            # step 2: get owners share, theta
            delegator.revenue_token_holdings += owners_share * revenue
        
        #  step 3: distribute non-owners share
        # print(f'{delegator.shares=}')
        delegator.revenue_token_holdings += delegator.shares * revenue_per_share
    
    key = 'delegators'
    value = s['delegators']
    return key, value
