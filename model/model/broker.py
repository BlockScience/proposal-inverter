class Broker:
    # autoincrementing id.
    broker_counter = 0

    def leaver_status(self, threshold):
        return self.epoch_counter<=threshold

    def iterate_epoch_counter(self):
        print(self.epoch_counter)
        self.epoch_counter +=1

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

        # the number of consequitive epochs the broker has been a member
        self.epoch_counter = 0

        # member of the agreement (True/False), in set B
        self.member = True

        # how long the broker has been attached to the stream
        self.time_attached = 0

        # is the broker allowed to leave?
        self.allowed_to_leave = False

        Broker.broker_counter += 1
