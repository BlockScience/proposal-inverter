class Broker:
    def __init__(self):
        ## initialize broker state
        self.claimable_funds = 0    # money that can be claimed by this broker
        self.stake = 5              # amount of money that is put in escrow, broker loses it if they break the rules
        self.holdings = 0           # amount of money this broker has
        self.member = True          # member of the agreement (True/False), in set B

    # skip for now, agreement is already deployed    
    # def deploy_agreement(self):
    #     return 0
    