from dataclasses import dataclass
from datetime import date
from typing import List, TypedDict


@dataclass
class CurrencyCode:
    code: str

    def __post_init__(self):
        self.code = self.code.capitalize()
        if len(self.code) != 3:
            err_msg = "Currency code uses ISO-4217 standard (3 characters expected)."
            raise ValueError(err_msg)


class Rate(TypedDict):
    no: str
    effective_date: date
    bid: float
    ask: float


@dataclass
class CurrentExchangeRateRequest:
    table: str
    currency_code: CurrencyCode
    top_count: int
    start_date: date
    end_date: date


@dataclass
class CurrentExchangeRateResponse:
    code: CurrencyCode
    currency: str
    rates: List[Rate]
