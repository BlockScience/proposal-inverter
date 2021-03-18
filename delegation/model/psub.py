
from .model.add_delegator import instantiate_delegate, should_instantiate_delegate

from .model.delegator_behaviors import (act,
                                        may_act_this_timestep)

from .model.revenue import revenue_amt, store_revenue, distribute_revenue

from .model.private_price import compute_and_store_private_prices

from .model.delegator_behaviors_bookkeeping import (account_global_state_from_delegator_states, 
                                                    store_reserve,
                                                    store_supply,
                                                    store_spot_price)


psubs = [
    # {
    #     'label': 'Update Time Attached',
    #     'policies': {
    #     },
    #     'variables': {
    #         'delegators': update_time_attached  # helpful for vesting
    #     }
    # },
    {
        'label': 'Revenue Arrival Process',
        'policies': {
            'revenue_amt': revenue_amt  # how much is paid in.
        },
        'variables': {
            'period_revenue': store_revenue,
        },
    },
    {
        'label': 'Distribute Revenue',
        'policies': {
        },
        'variables': {
            'delegators': distribute_revenue,
        }
    },
    {
        # if there's a vacant spot, flip a coin
        # (heads, they join, tails nobody joins)
        'label': 'Add Delegator',
        'policies': {
            'should_instantiate_delegate': should_instantiate_delegate
            },
        'variables': {
            'delegators': instantiate_delegate,
            },
    },
    {
        'label': 'Compute and Store Private Prices',
        'policies': {            
        },
        'variables': {
            'delegators': compute_and_store_private_prices,
        },
    },
    {
        'label': 'Delegator Behaviors',
        'policies': {
            # outputs ordered list of acting delegatorIds this timestep
            'may_act_this_timestep': may_act_this_timestep
        },
        'variables': {
            'delegators': act,
        },
    },
    {
        'label': 'Delegator Behaviors Bookkeeping',
        'policies': {
            'account_global_state_from_delegator_states': account_global_state_from_delegator_states
        },
        'variables': {
            'reserve': store_reserve,
            'supply': store_supply,
            'spot_price': store_spot_price,
        },
    },
]

