from __future__ import annotations

import math

from pydantic import BaseModel

import chapter1.util as util
from chapter1.enums import QuotationBasis, DayCountConvention


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

        rate = self.change_periodicity(rate=self.rate, old=self.periodicity, new=periodicity)
        return InterestRate.create(rate=rate, periodicity=periodicity, quotation_basis=self.quotation_basis,
                                   day_count_convention=self.day_count_convention)

    def __eq__(self, other: InterestRate):
        if self.__class__ is other.__class__:
            return self.model_dump() == other.model_dump()

        return TypeError(f'Unexpected type [{type(other)}] of [{other}]')

    @staticmethod
    def create(*, rate: float, periodicity=2, quotation_basis=QuotationBasis.AddOnRate,
               day_count_convention=DayCountConvention.Actual360) -> InterestRate:
        return InterestRate(rate=rate, periodicity=periodicity, quotation_basis=quotation_basis,
                            day_count_convention=day_count_convention)

    @staticmethod
    def dr_to_aor(*, dr: float, days: int, days_in_year: int) -> float:
        return (days_in_year * dr) / (days_in_year - (days * dr))

    @staticmethod
    def change_periodicity(*, rate: float, old: int, new: int) -> float:
        return (math.pow(math.pow((1 + rate / old), old), 1 / new) - 1) * new

    @staticmethod
    def dr_to_bey(*, dr: float, days: int, days_in_year: int) -> float:
        return (365 * dr) / (days_in_year - (days * dr))
