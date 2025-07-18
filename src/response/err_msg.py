from settings import settings


def not_found(resource: str):
    return f"{resource.capitalize()} was not found"


INVALID_EMAIL = f"Only emails ending with {settings.org_email} are accepted"
INTERNAL_SERVER_ERR = "Internal server error"
EMAIL_EXIST = "This email already exists"
DUPLICATE_ENTRY = "Duplicate entry – this value already exists"
FOREIGN_KEY_VIOLATION = (
    "Foreign key constraint violation – referenced item does not exist"
)
DB_ERR = "Database integrity error"
