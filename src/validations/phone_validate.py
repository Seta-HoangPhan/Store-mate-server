import re

from response import err_msg


def phone_validate(v: str):
    v = re.sub(r"[ \-]", "", v)  # Remove spaces and dashes

    # Regex: after +84 requires 3|5|7|8|9 and then 8 digits
    if not re.fullmatch(r"\+84(3|5|7|8|9)\d{8}", v):
        raise ValueError(err_msg.INVALID_PHONE)
    return v
