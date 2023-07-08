import util
from interest_rate import InterestRate


class TBills:
    def __init__(self, discount_rate_pct: float, maturity_weeks: int):
        self.discount_rate: float = discount_rate_pct / 100
        self.maturity_weeks: int = maturity_weeks
        self._days = self.maturity_weeks * 7
        self._days_in_year = 360
        self._periodicity = util.to_int(52 / self.maturity_weeks)

        self.pv = 100 * (1 - (self.discount_rate * self._days / self._days_in_year))
        self.investment_rate = InterestRate.dr_to_aor(dr=self.discount_rate, days=self._days,
                                                      days_in_year=self._days_in_year)
        if self.maturity_weeks >= 26:  # as reported officially
            self.investment_rate = InterestRate.change_periodicity(self.investment_rate, self._periodicity, 2)

    def __repr__(self):
        return f'Term: [{self.maturity_weeks}] weeks, discount_rate: [{self.discount_rate * 100:0.4f}], ' \
               f'Investment Rate: [{self.investment_rate}], Price (per $100 in par value): [{self.pv:0.4f}]'
