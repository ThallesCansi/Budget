from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, StringConstraints

Color = Annotated[str, StringConstraints(pattern=r"^#[0-9a-fA-F]{6}$")]
Icon = Annotated[str, StringConstraints(pattern=r"^[a-z0-9-]{1,40}$")]
Cents = Annotated[int, Field(ge=1, le=1_000_000_000_00)]
SignedCents = Annotated[int, Field(ge=-1_000_000_000_00, le=1_000_000_000_00)]


def _require_text(value: str) -> str:
    value = " ".join(value.split())
    if not value:
        raise ValueError("Não pode ficar em branco.")
    return value


Name = Annotated[str, StringConstraints(max_length=60), AfterValidator(_require_text)]
Label = Annotated[str, StringConstraints(max_length=80), AfterValidator(_require_text)]
PersonName = Annotated[str, StringConstraints(max_length=120), AfterValidator(_require_text)]
Description = Annotated[str, StringConstraints(max_length=140), AfterValidator(_require_text)]


class Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
