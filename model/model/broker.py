class Broker:
    # autoincrementing id.
    broker_counter = 0

    def __init__(self):
        # initialize broker state
        self.id = Broker.broker_counter

        # money that can be claimed by this broker
        self.claimable_funds = 0

        # amount of money that is put in escrow,
        # broker loses it if they break the rules
        self.stake = 5

        # amount of money this broker has
        self.holdings = 0

        # member of the agreement (True/False), in set B
        self.member = True
        Broker.broker_counter += 1
