from decimal import Decimal
from typing import Optional

from response import err_msg


def validate_discount(v: Optional[Decimal]):
    if v is None:
        return v

    rounded = v.quantize(Decimal("0.01"))

    if rounded < 0 or rounded > Decimal("100.00"):
        raise ValueError(err_msg.INVALID_DISCOUNT)

    return rounded
