from typing import Union

import numpy as np
import numpy_financial as npf
import pydantic

from interval import Interval


def to_int(number: Union[int, float], throw=True) -> int:
    if isinstance(number, int):
        return number

    if isinstance(number, float):
        if number.is_integer():
            return int(number)

        if throw:
            raise ValueError(f'Float number: [{number:0.6f}] can not be converted to int without data loss')

        else:
            return int(number)

    raise ValueError(f'Expected either int or float, but got [{number}] of type [{type(number)}]')


def to_pct_str(number: Union[int, float], precision=4) -> str:
    if isinstance(number, int):
        return f'{number * 100}%'

    if isinstance(number, float):
        if number.is_integer():
            return f'{int(number) * 100}%'

        return f'{number * 100:.{precision}}%'

    raise ValueError(f'Expected either an int or float, but received [{number}] of type [{type(number)}]')


@pydantic.validate_arguments
def get_bond_payments(face_value: float, coupon_rate_pct: float, coupon_period: Interval, maturity: Interval) \
        -> list[float]:
    """
    To get all the payments received by the investor assuming bond is held till maturity and issuer doesn't default
    Args:
        face_value: face value of the bond
        coupon_rate_pct: Annual coupon rate of the bond on each coupon:
        coupon_period: Interval between successive coupon payments
        maturity: Maturity of bond

    Returns:
        List of all payments received by the investor
    """
    each_coupon_payment = (face_value * coupon_rate_pct / 100) * coupon_period.fraction_of_year()
    all_coupon_payments = [each_coupon_payment] * (maturity / coupon_period)
    return all_coupon_payments[:-1] + [all_coupon_payments[-1] + face_value]


@pydantic.validate_arguments
def get_bond_cash_flow(mkt_price: float, face_value: float, coupon_rate_pct: float, coupon_period: Interval,
                       maturity: Interval) -> list[float]:
    """
    Args:
        mkt_price: current market price for bond
        face_value: face value of the bond
        coupon_rate_pct: Annual coupon rate of the bond on each coupon:
        coupon_period: Interval between successive coupon payments
        maturity: Maturity of bond

    Returns:
        List of all cash flows
    """
    return [-mkt_price] + get_bond_payments(face_value, coupon_rate_pct, coupon_period, maturity)


@pydantic.validate_arguments
def ytm(mkt_price: float, face_value: float, coupon_rate_pct: float, coupon_period: Interval, maturity: Interval) \
        -> float:
    """
    Args:
        mkt_price: current market price for bond
        face_value: face value of the bond
        coupon_rate_pct: Annual coupon rate of the bond on each coupon:
        coupon_period: Interval between successive coupon payments
        maturity: maturity in years/month

    Returns:
        object: Yield to maturity for the bond
    """

    return npf.irr(get_bond_cash_flow(mkt_price, face_value, coupon_rate_pct, coupon_period, maturity)) \
        * 100 / coupon_period.fraction_of_year()


@pydantic.validate_arguments
def rcy(mkt_price: float, face_value: float, coupon_rate_pct: float, coupon_period: Interval, maturity: Interval,
        reinvestment_rate: float) -> float:
    """
    To calculate RCY (Realized Compounded Yield):
    It calculates the net return on:
    1) Holding a bond and getting each coupon payment on time
    2) And investing each coupon and realizing a return of @inv_rate on investing these coupons

    Args:
        mkt_price: current market price for bond
        face_value: face value of the bond
        coupon_rate_pct: coupon rate of the bond
        coupon_period: Interval between successive coupon payments
        maturity: maturity in years/month
        reinvestment_rate: the annual rate of return on coupons

    Returns:
        object: Realized Compounded Yield for the bond
    """
    coupon = (face_value * coupon_rate_pct / 100) * coupon_period.fraction_of_year()
    growth_rate = 1 + reinvestment_rate * coupon_period.fraction_of_year() / 100

    coupon_count = maturity / coupon_period
    coupon_fv = coupon * np.power(growth_rate, np.arange(coupon_count))
    total_sum_capitalized = np.sum(coupon_fv) + face_value

    return (np.power(total_sum_capitalized / mkt_price, 1 / coupon_count) - 1) \
        * 100 / coupon_period.fraction_of_year()


@pydantic.validate_arguments
def price(face_value: float, coupon_rate_pct: float, bond_yield: float, coupon_period: Interval, maturity: Interval) \
        -> float:
    """

    Args:
        face_value: Face values of the bond
        coupon_rate_pct: Annual coupon rate
        bond_yield: YTM (Yield To Maturity) of the bond
        coupon_period: Interval between successive coupon payments
        maturity: Tenor or Maturity of the bond
    Returns:
        Based on the yield to maturity (and all other parameters), returns the current price
    """
    # get the cash flow from first coupon to till last (coupon + face value)
    # - 1st argument is a dummy one, gets ignored anyway
    cash_flow = np.array(get_bond_cash_flow(0, face_value, coupon_rate_pct, coupon_period, maturity)[1:])
    discount_rate = 1 + bond_yield * coupon_period.fraction_of_year() / 100
    discount_factors = np.power(discount_rate, np.arange(1, len(cash_flow) + 1))
    discounted_cash_flows = cash_flow / discount_factors
    return sum(discounted_cash_flows)
