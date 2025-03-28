import math
from scipy.optimize import brentq
from scipy.stats import norm


class Options:
    def __init__(self,
                 stock_prices: list,
                 exercise_prices: list,
                 time_to_maturity_days: float,
                 risk_free_rate_proc: float,
                 stock_volatility_proc: float = None,
                 debug: bool = False):

        if len(stock_prices) != len(exercise_prices):
            raise ValueError("Stock prices and exercise prices need to be same length")

        self.options = [
            Option(stock_prices[i],
                   exercise_prices[i],
                   time_to_maturity_days,
                   risk_free_rate_proc,
                   stock_volatility_proc,
                   debug=debug
                   ) for i in range(0, len(stock_prices))
        ]

    def call_prices(self):
        return [i.call_price() for i in self.options]

    def put_prices(self):
        return [i.put_price() for i in self.options]

    def call_intrinsic_values(self):
        return [i.call_intrinsic_value() for i in self.options]

    def put_intrinsic_values(self):
        return [i.put_intrinsic_value() for i in self.options]

    def call_price_implied_volatilises(self, market_price: list):
        if len(market_price) != len(self.options):
            raise ValueError(f"Market prices need to be list of length {len(self.options)}")

        return [self.options[i].call_price_implied_volatility(market_price[i]) for i in range(0, len(self.options))]


class Option:
    def __init__(self,
                 stock_price: float,
                 exercise_price: float,
                 time_to_maturity_days: float,
                 risk_free_rate_proc: float,
                 stock_volatility_proc: float = None,
                 debug: bool = False):

        self.stock_price = stock_price
        self.exercise_price = exercise_price
        self.T = time_to_maturity_days / 365
        self.r = risk_free_rate_proc / 100
        self.sigma = stock_volatility_proc / 100 if stock_volatility_proc else None

        if debug and self.sigma:
            print(f"d1: {self._d1(self.sigma)}")
            print(f"d2: {self._d2(self.sigma)}")
            print(f"N(d1): {self._cdf(self._d1(self.sigma))}")
            print(f"N(d2): {self._cdf(self._d2(self.sigma))}")
            print(f"Call intrinsic: {self.call_intrinsic_value()}")
            print(f"Put intrinsic: {self.put_intrinsic_value()}")
            print(f"Call price: {self.call_price()}")
            print(f"Put price: {self.put_price()}")

    def _cdf(self, value):
        return norm.cdf(value)

    def _d1(self, sigma):
        s = self.stock_price
        k = self.exercise_price

        return (math.log(s / k) + (self.r + 0.5 * sigma ** 2) * self.T) / (sigma * math.sqrt(self.T))

    def _d2(self, sigma):
        d1 = self._d1(sigma)
        adjustment = sigma * math.sqrt(self.T)
        return d1 - adjustment

    def _present_value_strike(self, sigma, sign=1):
        d2 = self._d2(sigma)
        disc = math.exp(-self.r * self.T)

        return self.exercise_price * disc * norm.cdf(sign * d2)

    def _spot_value(self, sigma, sign=1):
        d1 = self._d1(sigma)

        return self.stock_price * norm.cdf(sign * d1)

    def call_price(self):
        if not self.sigma:
            raise ValueError("Stock volatility must be set.")
        s = self._spot_value(self.sigma)
        k = self._present_value_strike(self.sigma)
        return s - k

    def put_price(self):
        if not self.sigma:
            raise ValueError("Stock volatility must be set.")
        s = self._spot_value(self.sigma, sign=-1)
        k = self._present_value_strike(self.sigma, sign=-1)
        return k - s

    def call_intrinsic_value(self):
        return max(0, self.stock_price - self.exercise_price)

    def put_intrinsic_value(self):
        return max(0, self.exercise_price - self.stock_price)

    def _call_price_difference(self, sigma, market_price):
        return self._spot_value(sigma) - self._present_value_strike(sigma) - market_price

    def call_price_implied_volatility(self, market_price):
        return brentq(lambda sigma: self._call_price_difference(sigma, market_price), 0.01, 2.0)



if __name__ == "__main__":
    option = Option(
        100,
        90,
        182.5,
        4,
        35,
        debug=True
    )

    print(f"Implied volatility (%): {round(option.call_price_implied_volatility(16.32),2)*100}")
