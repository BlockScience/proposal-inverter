def payment_to_unallocated(params, step, prev_states, state, _input):

    value = state['unallocated_funds'] + _input['payment_amt']
    key = 'unallocated_funds'

    return key, value

## rendered this uncessary by taking total out of explicit state (still computable as sum)
# def payment_to_total(params, step, prev_states, state, input):

#     value = state['total_funds'] + input['amt']
#     key = state['total_funds']

#     return key, value
