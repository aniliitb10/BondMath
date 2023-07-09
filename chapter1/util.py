from typing import Union


def to_int(number: Union[int, float], throw=True) -> int:
    if type(number) == int:
        return number

    if type(number) == float:
        if number.is_integer():
            return int(number)

        if throw:
            raise ValueError(f'Float number: [{number:0.6f}] can not be converted to int without data loss')

        else:
            return int(number)

    raise ValueError(f'Expected either int or float, but got [{number}] of type [{type(number)}]')


def to_pct_str(number: Union[int, float], precision=4) -> str:
    if type(number) == int:
        return f'{number * 100}%'

    if type(number) == float:
        if number.is_integer():
            return f'{int(number) * 100}%'

        return f'{number * 100:.{precision}}%'

    raise ValueError(f'Expected either an int or float, but received [{number}] of type [{type(number)}]')
