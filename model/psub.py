# from .behavior import update_a
from .model.allocate_payments import (allocated_funds, unallocated_funds,
                                      check_brokers,
                                      allocate_funds_to_member_brokers
                                      )

from .model.leaves import (should_leaves, leaves,
                           decrement_allocated_funds_due_to_leaves,
                           increment_unallocated_funds_due_to_forfeit_stake,
                           allowed_to_leave)

from .model.joins import should_join, joins

from .model.helper_functions import count_brokers

from .model.claims import (should_make_claims, make_claims,
                           decrement_allocated_funds_by_claims)

from .model.bookkeeping import update_time_attached, total_broker_stake

from .model.payments import payment_to_unallocated

from .behavior import payment_amt

from .model.add_delegator import instantiate_delegate, should_instantiate_delegate

from .model.delegator_behaviors import (act,
                                        may_act_this_timestep)

from .model.revenue import revenue_amt, store_revenue, distribute_revenue

from .model.private_price import compute_and_store_private_prices

from .model.delegator_behaviors_bookkeeping import (compute_cliff_vested_shares,
                                                    account_global_state_from_delegator_states,
                                                    store_reserve,
                                                    store_supply,
                                                    store_spot_price)

psubs = [
    {
        'label': 'Update Time Attached',
        'policies': {
        },
        'variables': {
            'brokers': update_time_attached
        }
    },
    {
        'label': 'Payments',
        'policies': {
            'payment_amt': payment_amt  # how much is paid in.
        },
        'variables': {
            'unallocated_funds': payment_to_unallocated
        },
    },
    {
        'label': 'Allocate Payments',
        'policies': {
            'check_brokers': check_brokers
        },
        'variables': {
            'allocated_funds': allocated_funds,       # A
            'unallocated_funds': unallocated_funds,   # R
            'brokers': allocate_funds_to_member_brokers,
        }
    },
    {
        'label': 'Claims',
        'policies': {
            'should_make_claims': should_make_claims
        },
        'variables': {
            'brokers': make_claims,
            'allocated_funds': decrement_allocated_funds_by_claims
        },
    },
    {
        'label': 'Allowed to Leave',
        'policies': {},
        'variables': {
            'brokers': allowed_to_leave
        },
    },
    {
        'label': 'Leaves',
        'policies': {
            'should_leaves': should_leaves
            },
        'variables': {
            'brokers': leaves,
            'allocated_funds': decrement_allocated_funds_due_to_leaves,
            'unallocated_funds': increment_unallocated_funds_due_to_forfeit_stake,
            'num_member_brokers': count_brokers
            }
    },
    {
        # if there's a vacant spot, flip a coin
        # (heads, they join, tails nobody joins)
        'label': 'Joins',
        'policies': {
            'should_join': should_join
            },
        'variables': {
            'brokers': joins,
            'num_member_brokers': count_brokers,
            },
    },
    {
        'label': 'Bookkeeping',
        'policies': {
        },
        'variables': {
            'total_broker_stake': total_broker_stake,
            'brokers': update_time_attached
        }

    },
    {
        'label': 'Update Vested Shares',
        'policies': {
        },
        'variables': {
            # 'delegators': compute_half_life_vested_shares
            'delegators': compute_cliff_vested_shares
        }
    },
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
