import random
""" A Delegator is an actor who delegates native tokens to the revenue sharing pool
for shares in the revenue stream. """


class Delegator:
    # autoincrementing id.
    delegate_counter = 0

    def __init__(self, shares=0, reserve_token_holdings=0, expected_revenue=0, discount_rate=.9,
                 delegator_activity_rate=0.5, minimum_shares=0):
        # initialize delegator state
        self.id = Delegator.delegate_counter

        # these can vest--either cliff, or half-life 
        # shares is stored as dict, {key=timestep, value=num_shares} for vesting purposes.
        self._shares = {0: shares}

        # Tokens the delegator is holding, but in the denomination the revenues are paid in.
        # (USD token or any other token)
        self.revenue_token_holdings = 0

        # Amount of token the delegator is holding, in same denomination as Reserve (R).
        self.reserve_token_holdings = reserve_token_holdings

        self.expected_revenue = expected_revenue

        # used to discount cash flows. 1 / (1 - discount_rate)
        self.time_factor = 1 / (1 - discount_rate)
        self.delegator_activity_rate = delegator_activity_rate

        # dict -- {key=timestep, value=price}
        self.private_prices = {}

        self.minimum_shares = minimum_shares

        # increment counter for next delegator ID
        Delegator.delegate_counter += 1

    
   
    # member of the sharing pool (True/False)
    def is_member(self):
        return self.shares > 0

    
    def shares(self):
        return sum(s for s in self._shares.values())

    def set_shares(self, timestep, shares):
        self._shares[timestep] = shares

    # select vesting function here.
    def vested_shares(self):
        return self.vested_shares_cliff

   
    def vested_shares_cliff(self):
        """ calculate how many shares are vested using cliff vesting """
        return self._vested_shares

    
    def vested_shares_half_life(self):
        """ calculate how many shares are vested using half_life vesting """
        return self._vested_shares


    def dividend_value(self, supply, owners_share, reserve_to_revenue_token_exchange_rate):
        """ take belief of revenue * your shares / total shares """
        revenue_per_period_per_share = 0
        # if supply > 0:
        #     # this is always 0 if self.shares = 0
        #     revenue_per_period_per_share = self.expected_revenue * (1 - owners_share) * self.shares / supply

        assert(supply > 0)

        # owners share is resolved before any share percentage calculation
        revenue_per_period_per_share = self.expected_revenue * (1 - owners_share) / supply

        reserve_asset_per_period_per_share = revenue_per_period_per_share * \
            reserve_to_revenue_token_exchange_rate

        reserve_asset_per_share_time_corrected = reserve_asset_per_period_per_share * \
            self.time_factor

        # print(f'dividend_value: {self.id=}, {supply=}, {self.expected_revenue=}, {revenue_per_period_per_share=}, \
        #     {reserve_asset_per_period_per_share=}, {reserve_asset_per_share_time_corrected=}')
        return reserve_asset_per_share_time_corrected

    
    def will_act(self):
        # flip a uniform random variable, compare to activity, rate, if it's below, then set to act.
        rng = random.random()
        return rng < self.delegator_activity_rate


    def buy_or_sell(self, supply, reserve, spot_price,
                    mininum_required_price_pct_diff_to_act,
                    timestep):
        """
            compare private price to spot price -- just changed
            look at difference between spot and private price.
            if it's low, buy.  close, do nothing.  high, sell
            if sell, compute amount of shares to burn such that realized price is equal to private price
            if that amount is > amt i have, burn it all (no short sales)
        """                    
        private_price = self.private_prices[timestep]
        pct_price_diff = 0
        if spot_price > 0:
            pct_price_diff = abs((private_price - spot_price) / spot_price)

        created_shares = 0
        added_reserve = 0
        # print(f'buy_or_sell: DELEGATOR {self.id} -- {private_price=}, {spot_price=}, {pct_price_diff=}, {self.reserve_token_holdings=}, {self.shares=}')
        if pct_price_diff < mininum_required_price_pct_diff_to_act:
            # don't act.
            return created_shares, added_reserve

        if private_price > spot_price:
            # print(f'buy_or_sell: DELEGATOR {self.id} -- WANTS TO BUY')
            # BUY ###
            # figure out how much delegator spending, then buy it

            # this formula, not used, is when the delegator buys until private_price == realized_price
            # added_reserve = (private_price * supply * (private_price * supply - 2 * reserve))/reserve
            # created_shares = supply * ((1 + added_reserve / reserve) ^ (1/2)) - supply
            # assert(private_price == realized_price)

            # this formula stops buying when spot_price is equal to private_price
            added_reserve = ((private_price ** 2) * (supply ** 2) - (4 * reserve ** 2)) / (4 * reserve)

            # can't spend reserve you don't have
            if added_reserve > self.reserve_token_holdings:
                added_reserve = self.reserve_token_holdings
            created_shares = supply * ((1 + added_reserve / reserve) ** (1/2)) - supply


            # then update the state

            # delegator:
            #   increasing shares
            #   decreasing reserve_token_holdings
            # system:
            #   increasing total shares
            #   increasing reserve

        elif private_price < spot_price:
            # SELL ###
            # print(f'buy_or_sell: DELEGATOR {self.id} -- WANTS TO SELL')
            burned_shares = ((2 * reserve * supply) - (private_price * supply ** 2)) / (2 * reserve)

            shares_count = self.shares()
            # can't burn shares you don't have.
            if burned_shares > shares_count:
                burned_shares = shares_count

            # can't burn shares you're not allowed to burn (original delegator's 10)
            if shares_count - burned_shares < self.minimum_shares:
                burned_shares = shares_count - self.minimum_shares

            created_shares = -burned_shares
            # payout
            reserve_paid_out = reserve - reserve * (1 - burned_shares / supply) ** 2
            added_reserve = -reserve_paid_out
            # delegator:
            #   decreasing shares
            #   increasing reserve_token_holdings
            # system:
            #   decreasing total shares
            #   decreasing reserve
        
        # final_spot_price = (2 * (reserve + added_reserve)) / (supply + created_shares)
        # acceptable_tolerance = mininum_required_price_pct_diff_to_act
        # diff = abs(private_price - final_spot_price)
        # print(f'buy_or_sell: DELEGATOR {self.id} -- {private_price=}, {final_spot_price=}, {diff=}, {acceptable_tolerance=}')
        
        # NOTE: we cannot assert(diff < acceptable_tolerance) for all cases because the diff won't be less than acceptable_tolerance in all cases
        # for example: the delegator is not allowed to sell due to a minimum number of shares.
        # assert(diff < acceptable_tolerance)

        self.reserve_token_holdings -= added_reserve
        self.set_shares(timestep, created_shares)

        # if created_shares > 0:
        #     print(f'buy_or_sell: DELEGATOR {self.id} -- BOUGHT {created_shares=} for {added_reserve=}')
        # elif created_shares < 0:
        #     print(f'buy_or_sell: DELEGATOR {self.id} -- SOLD {created_shares=} for {added_reserve=}')

        return created_shares, added_reserve

# test that i input a value of dR, i get the right value of dS
