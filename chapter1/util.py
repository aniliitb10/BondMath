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
