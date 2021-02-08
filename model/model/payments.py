def payment_to_unallocated(params, step, sL, s, inputs):

    key = 'unallocated_funds'
    value = s['unallocated_funds'] + inputs['payment_amt']

    return key, value
