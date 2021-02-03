def get_member_brokers(brokers):
    return {broker_id: broker for broker_id, broker in brokers.items()}


def count_members(brokers):
    value = sum(1 for broker in brokers.values() if broker.member)
    return value
