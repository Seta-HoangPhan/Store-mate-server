def not_found(resource: str):
    return f"{resource.capitalize()} was not found"


def exist(resource: str):
    return f"{resource.capitalize()} already exist"


def missing(resource: str):
    return f"Missing {resource.capitalize()}"


# authentication error messages
EXIST_FIRST_ADMIN = "The first admin user already exists"
INVALID_PHONE = "Invalid phone number format"
EMAIL_EXIST = "This email already exists"
PHONE_EXIST = "This phone number already exists"
NO_OTP_REQUEST = "No OTP request found"
INVALID_OTP = "The provided OTP is invalid"
EXPIRED_OTP = "OTP has expired, please request a new one"
INVALID_PASSWORD = "The provided password is invalid"
INVALID_TOKEN = "Invalid authentication credentials"
MISSING_TOKEN = "Not authenticated"
NOT_FOUND_USER_OR_INVALID_TOKEN = "User not found or invalid token"

CAN_NOT_DELETE_ROOT_ADMIN = "Root admin cannot be deleted"

UPLOAD_CLOUDINARY_FAILED = "Failed to upload image or file"
INTERNAL_SERVER_ERR = "Internal server error"
DUPLICATE_ENTRY = "Duplicate entry – this value already exists"
FOREIGN_KEY_VIOLATION = (
    "Foreign key constraint violation – referenced item does not exist"
)
DB_ERR = "Database integrity error"
FORBIDDEN = "Access denied. Insufficient permissions"

INVALID_DECIMAL = "Price must have at most 10 digits in total, including 2 decimal places (e.g., 99999999.99)"
INVALID_DISCOUNT = "Discount should be from 0.00% to 100.00%"
