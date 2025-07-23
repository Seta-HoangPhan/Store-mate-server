import re

from response import err_msg


def validate_phone(v: str):
    v = re.sub(r"[ \-]", "", v)  # Remove spaces and dashes

    # Regex: after +84 requires 3|5|7|8|9 and then 8 digits
    if not re.fullmatch(r"\+84(3|5|7|8|9)\d{8}", v):
        raise ValueError(err_msg.INVALID_PHONE)
    return v


# phones can be list[str] or list[Schema]
def validate_phone_list(phones: list):
    if len(phones) == 0:
        raise ValueError(err_msg.missing("Phone number"))

    normalized_phones = []
    if isinstance(phones[0], str):
        for phone in phones:
            valid_phone = validate_phone(phone)
            normalized_phones.append(valid_phone)
    else:
        for schema in phones:
            id = getattr(schema, "id")
            phone = getattr(schema, "phone")
            valid_phone = validate_phone(phone)
            normalized_phones.append({"id": id, "phone": valid_phone})

    return normalized_phones
