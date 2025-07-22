from pydantic import BaseModel


def convert_update_data(data: BaseModel):
    return data.model_dump(exclude_unset=True, exclude_none=True)
