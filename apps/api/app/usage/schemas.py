from typing import Literal

from pydantic import BaseModel


class UsageStatus(BaseModel):
    status: Literal["reserved", "charged", "released"]
    uses: int = 1
    reference: str

