class Broker:
    # autoincrementing id.
    broker_counter = 0

    def __init__(self):
        # initialize broker state
        self.id = Broker.broker_counter

        # money that can be claimed by this broker
        self.claimable_funds = 0

        # amount of money that is put in escrow,
        # broker loses it if they leave when not allowed
        self.stake = 5

        # amount of money this broker has
        self.holdings = 0

        # member of the agreement (True/False)
        self.member = True

        # how long the broker has been attached to the agreement
        self.time_attached = 0

        # is the broker allowed to leave?
        self.allowed_to_leave = False

        Broker.broker_counter += 1
