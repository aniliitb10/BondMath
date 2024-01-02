from __future__ import annotations

import math

from pydantic import BaseModel

import util as util
from enums import QuotationBasis, DayCountConvention


class InterestRate(BaseModel):
    rate: float
    periodicity: int
    quotation_basis: QuotationBasis
    day_count_convention: DayCountConvention

    def to_aor(self) -> InterestRate:
        """
        To get the same InterestRate but with Add on Rate convention
        """
        if self.quotation_basis == QuotationBasis.AddOnRate:
            return self

        days_in_year = self.day_count_convention.days_in_year()
        aor = self.dr_to_aor(dr=self.rate, days=util.to_int(days_in_year / self.periodicity), days_in_year=days_in_year)
        return InterestRate.instance(rate=aor, periodicity=self.periodicity, quotation_basis=QuotationBasis.AddOnRate,
                                     day_count_convention=self.day_count_convention)

    def to_periodicity(self, periodicity: int) -> InterestRate:
        """
        To change the Interest Rate to the give periodicity
        :param periodicity: target periodicity
        :return: Instance of InterestRate with given @periodicity
        """
        if self.periodicity == periodicity:
            return self

        rate = self.change_periodicity(rate=self.rate, old=self.periodicity, new=periodicity)
        return InterestRate.instance(rate=rate, periodicity=periodicity, quotation_basis=self.quotation_basis,
                                     day_count_convention=self.day_count_convention)

    def __eq__(self, other: InterestRate):
        if self.__class__ is other.__class__:
            return self.model_dump() == other.model_dump()

        return TypeError(f'Unexpected type [{type(other)}] of [{other}]')

    @staticmethod
    def instance(*, rate: float, periodicity=2, quotation_basis=QuotationBasis.AddOnRate,
                 day_count_convention=DayCountConvention.Actual360) -> InterestRate:
        """
        :param rate: The interest rate to initialize with
        :param periodicity: the number of times interest rate compounds in a year (e.g. for semi-annual, it is 2)
        :param quotation_basis: Either Add on Rate or Discount Rate
        :param day_count_convention: based on the security, region (could be 360 or 365)
        :return: and InterestRate instance
        """
        return InterestRate(rate=rate, periodicity=periodicity, quotation_basis=quotation_basis,
                            day_count_convention=day_count_convention)

    @staticmethod
    def dr_to_aor(*, dr: float, days: int, days_in_year: int) -> float:
        """
        :param dr: discount rate
        :param days: number of days to consider for the interest rate
        :param days_in_year: as per the convention, could be 360, 365 or 366
        :return: Add on Rate for the discount Rate
        """
        return (days_in_year * dr) / (days_in_year - (days * dr))

    @staticmethod
    def change_periodicity(*, rate: float, old: int, new: int) -> float:
        """
        :param rate: The interest rate with @old periodicity
        :param old: old periodicity
        :param new: new periodicity
        :return: The interest rate with new periodicity
        """
        return (math.pow(math.pow((1 + rate / old), old), 1 / new) - 1) * new

    @staticmethod
    def dr_to_bey(*, dr: float, days: int, dr_days_in_year: int) -> float:
        """
        Conversion from Discount Rate to Bond Equivalent Yield (another name for Investment Rate)
        :param dr: Discount rate
        :param days: Days in year to consider for the interest rate
        :param dr_days_in_year: as the convention, could be 360, 365 or 366
        :return: Bond Equivalent Yield (another name for Investment Rate)
        """
        return (365 * dr) / (dr_days_in_year - (days * dr))
