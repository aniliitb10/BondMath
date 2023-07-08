from __future__ import annotations

import math

from pydantic import BaseModel

import util
from enums import QuotationBasis, DayCountConvention


class InterestRate(BaseModel):
    rate: float
    periodicity: int
    quotation_basis: QuotationBasis
    day_count_convention: DayCountConvention

    def to_aor(self) -> InterestRate:
        if self.quotation_basis == QuotationBasis.AddOnRate:
            return self

        days_in_year = self.day_count_convention.days_in_year()
        aor = self.dr_to_aor(dr=self.rate, days=util.to_int(days_in_year / self.periodicity), days_in_year=days_in_year)
        return InterestRate.create(rate=aor, periodicity=self.periodicity, quotation_basis=QuotationBasis.AddOnRate,
                                   day_count_convention=self.day_count_convention)

    def to_periodicity(self, periodicity: int) -> InterestRate:
        if self.periodicity == periodicity:
            return self

        rate = self.change_periodicity(self.rate, self.periodicity, periodicity)
        return InterestRate.create(rate=rate, periodicity=periodicity, quotation_basis=self.quotation_basis,
                                   day_count_convention=self.day_count_convention)

    @staticmethod
    def create(*, rate: float, periodicity=2, quotation_basis=QuotationBasis.AddOnRate,
               day_count_convention=DayCountConvention.Actual360) -> InterestRate:
        return InterestRate(rate=rate, periodicity=periodicity, quotation_basis=quotation_basis,
                            day_count_convention=day_count_convention)

    @staticmethod
    def dr_to_aor(*, dr: float, days: int, days_in_year: int) -> float:
        return (days_in_year * dr) / (days_in_year - (days * dr))

    @staticmethod
    def change_periodicity(rate: float, from_periodicity: int, to_periodicity: int) -> float:
        return (math.pow(math.pow((1 + rate / from_periodicity), from_periodicity),
                         1 / to_periodicity) - 1) * to_periodicity
