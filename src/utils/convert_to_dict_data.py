from pydantic import BaseModel


def convert_to_dict_data(Schema: BaseModel, data):
    return Schema.model_validate(data).model_dump()
