def not_found(resource: str):
    return f"{resource.capitalize()} was not found"


# authentication error messages
EXIST_FIRST_ADMIN = "The first admin user already exists"
INVALID_PHONE = "Invalid phone number format"
EMAIL_EXIST = "This email already exists"
NO_OTP_REQUEST = "No OTP request found"
INVALID_OTP = "The provided OTP is invalid"
EXPIRED_OTP = "OTP has expired, please request a new one"

INTERNAL_SERVER_ERR = "Internal server error"
DUPLICATE_ENTRY = "Duplicate entry – this value already exists"
FOREIGN_KEY_VIOLATION = (
    "Foreign key constraint violation – referenced item does not exist"
)
DB_ERR = "Database integrity error"
