from decimal import Decimal, ROUND_HALF_UP
from typing import Optional


def convert_decimal(v: Optional[Decimal]):
    if v is None:
        return v

    d = Decimal(str(v))
    return d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
