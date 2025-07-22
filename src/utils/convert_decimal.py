from decimal import Decimal
from typing import Optional


def convert_decimal(v: Optional[Decimal]):
    if v is None:
        return v

    return v.quantize(Decimal(0.01))
