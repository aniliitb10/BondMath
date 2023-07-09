import chapter1.util as util
from chapter1.interest_rate import InterestRate


class TBills:
    def __init__(self, maturity_weeks: int, discount_rate_pct: float):
        self.maturity_weeks: int = maturity_weeks
        self.discount_rate: float = discount_rate_pct / 100
        self._days = self.maturity_weeks * 7 if self.maturity_weeks != 26 else 183
        self._days_in_year = 360
        self._periodicity = util.to_int(52 / self.maturity_weeks)

        self.pv = 100 * (1 - (self.discount_rate * self._days / self._days_in_year))
        self.investment_rate: float = InterestRate.dr_to_bey(dr=self.discount_rate, days=self._days,
                                                             days_in_year=self._days_in_year)
        if self.maturity_weeks > 26:  # as reported officially
            self.investment_rate = InterestRate.change_periodicity(rate=self.investment_rate,
                                                                   old=self._periodicity, new=2)

    def __repr__(self):
        return f'Term: [{self.maturity_weeks}] weeks, Discount Rate: [{util.to_pct_str(self.discount_rate)}], ' \
               f'Investment Rate: [{util.to_pct_str(self.investment_rate)}], ' \
               f'Price (per $100 in par value): [{self.pv:0.6f}]'

    @property
    def investment_rate_pct(self) -> float:
        return self.investment_rate * 100
