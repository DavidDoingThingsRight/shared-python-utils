from typing import Any, cast, get_type_hints

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic_core.core_schema import ValidationInfo

from d_util.objects.DDateTime import DDate, DDateTime


class DBaseModel(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            DDateTime: lambda v: v.serialize(),
            DDate: lambda v: v.serialize(),
        }
    )

    @field_validator("*", mode="before")
    @classmethod
    def parse_ddatetime_fields(cls, v: Any, info: ValidationInfo) -> DDateTime:
        # info contains field info
        field_name = info.field_name
        field_name = cast(str, field_name)
        field_type = get_type_hints(cls).get(field_name)
        if field_type is DDateTime:
            # Since DDateTime is a custom type, this gets a bit complicated
            # Input will come as one of two cases:
            # 1. DDateTime object (when we are constructing the object normally)
            # 2. serialized datetime string (when we are deserializing from JSON)
            if isinstance(v, DDateTime):
                return v
            elif isinstance(v, str):
                # If it's a string, we assume it's a serialized datetime
                return DDateTime.deserialize(v)
            else:
                raise ValueError(f"Invalid type for field {info.field_name}: {type(v)}")
        return v

    @field_validator("*", mode="before")
    @classmethod
    def parse_ddate_fields(cls, v: Any, info: ValidationInfo) -> DDate:
        # info contains field info
        field_name = info.field_name
        field_name = cast(str, field_name)
        field_type = get_type_hints(cls).get(field_name)
        if field_type is DDate:
            # Since DDate is a custom type, this gets a bit complicated
            # Input will come as one of two cases:
            # 1. DDate object (when we are constructing the object normally)
            # 2. serialized date string (when we are deserializing from JSON)
            if isinstance(v, DDate):
                return v
            elif isinstance(v, str):
                # If it's a string, we assume it's a serialized date
                return DDate.deserialize(v)
            else:
                raise ValueError(f"Invalid type for field {info.field_name}: {type(v)}")
        return v
