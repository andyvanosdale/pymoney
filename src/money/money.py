"""Module providing a Money type for representing money and its calculations"""
import re


class Money:
    """Class representing a Money type (taken from Google's Cloud Money type)"""

    currencycode: str
    units: int
    nanos: int
    isnegative: bool
    ispositive: bool

    def __init__(self, currencycode: str, units: int, nanos: int):
        if nanos < -999_999_999 or nanos > 999_999_999:
            raise ValueError("nanos must be between -10^9 and 10^9", nanos)
        if units < 0:
            if nanos > 0:
                raise ValueError(
                    "nanos must be zero or negative when units is negative",
                    units,
                    nanos,
                )
        elif units > 0 and nanos < 0:
            raise ValueError(
                "nanos must be zero or positive when units is positive", units, nanos
            )

        self.currencycode = currencycode
        self.units = units
        self.nanos = nanos
        self.isnegative = units < 0 or nanos < 0
        self.ispositive = not self.isnegative

    def parse(self, money: str):
        """Parses a string into a Money"""
        matches = re.search(r"([A-Z]{3}) (-?)(\d+)\.(\d{1,9})", money)
        if matches is None:
            raise ValueError(
                'the value must be in the Money format "{CurrencyCode} {-}{Units}.{Nanos}"'
            )
        currencycode = matches.group(1)
        units = int(matches.group(3))
        nanos = int(matches.group(4))
        if matches.group(2) == "-":
            units = -units
        return Money(currencycode, units, nanos)

    def __add__(self, o):
        if self.currencycode != o.currencycode:
            raise ValueError(
                "Currency codes must match", self.currencycode, o.currencycode
            )

        sumnanos = self.nanos + o.nanos
        newnanos = (
            sumnanos % 1_000_000_000 if sumnanos >= 0 else sumnanos % -1_000_000_000
        )
        nanosoverflow = sumnanos // 1_000_000_000

        sumunits = self.units + o.units + nanosoverflow

        return Money(self.currencycode, sumunits, newnanos)

    def __radd__(self, o):
        if isinstance(o, int):
            return self + Money(self.currencycode, o, 0)

        raise ValueError("unsupported right operand", o)

    def __truediv__(self, dividend):
        if isinstance(dividend, int):
            return self / Money(self.currencycode, dividend, 0)

        if isinstance(dividend, Money):
            if self.currencycode != dividend.currencycode:
                raise ValueError(
                    "Currency codes must match", self.currencycode, dividend.currencycode
                )

            selfimpropernumerator = abs(self.units) * 1_000_000_000 + abs(self.nanos)
            dividendimpropernumerator = abs(dividend.units) * 1_000_000_000 + abs(
                dividend.nanos
            )
            newunits = selfimpropernumerator // dividendimpropernumerator
            newremainder = selfimpropernumerator % dividendimpropernumerator
            newnanos = newremainder // abs(dividend.units)
            if (self.isnegative or dividend.isnegative) and not (
                self.isnegative and dividend.isnegative
            ):
                newunits = -newunits
                newnanos = -newnanos
            return Money(self.currencycode, newunits, newnanos)

        raise ValueError("unsupported dividend", dividend)

    def __sub__(self, o):
        if isinstance(o, int):
            return self - Money(self.currencycode, o, 0)

        if isinstance(o, Money):
            newunits = self.units - o.units
            # TODO detect underflow
            newnanos = self.nanos - o.nanos
            return Money(self.currencycode, newunits, newnanos)

        raise ValueError("unsupported right operand", o)

    def __eq__(self, o):
        return (
            isinstance(o, Money)
            and self.currencycode == o.currencycode
            and self.units == o.units
            and self.nanos == o.nanos
        )

    def __str__(self):
        return (
            f"{self.currencycode} "
            f"{'-' if self.isnegative else ''}{abs(self.units)}.{abs(self.nanos)}"
        )

    def __repr__(self):
        return f'Money("{self.currencycode}", {self.units}, {self.nanos})'
