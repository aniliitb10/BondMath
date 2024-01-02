from enum import Enum


class QuotationBasis(Enum):
    AddOnRate = 'Add on Rate'
    DiscountRate = 'Discount Rate'


class DayCountConvention(Enum):
    Actual360 = 'Actual/360'
    Actual365 = 'Actual/365'
    Actual366 = 'Actual/366'
    Thirty360 = '30/360'

    def days_in_year(self) -> int:
        days = int(self.value.split('/')[1])
        if days not in (360, 365, 366):  # if further enums are added (unlikely), this must be revisited
            raise ValueError(f'Unexpected value extracted from enum: {self.name}')

        return days
