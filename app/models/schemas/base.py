from pydantic import BaseModel, ConfigDict, Field


def convert_field_to_upper_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )


def get_config() -> dict[str, any]:
    config = {
        "populate_by_name": True,
        "alias_generator": convert_field_to_upper_case,
    }

    return config


class AppModel(BaseModel):
    model_config = ConfigDict(**get_config())


class IDModelMixin(BaseModel):
    id_: int = Field(0, alias="id")
