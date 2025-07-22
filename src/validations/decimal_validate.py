from decimal import Decimal
from response import err_msg


def decimal_validate(v: Decimal):
    if v is None:
        return v

    rounded = v.quantize(Decimal("0.01"))  # Enforce 2 decimal places
    # Validate: max 8 digits before decimal, 2 after (total 10)
    sign, digits, exponent = rounded.as_tuple()
    digits_before = len(digits) + exponent if exponent < 0 else len(digits)
    if digits_before > 8:
        raise ValueError(err_msg.INVALID_DECIMAL)

    return rounded
