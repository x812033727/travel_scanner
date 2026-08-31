from datetime import date

from pydantic import BaseModel, Field, model_validator


class FlightStatusLookupCreate(BaseModel):
    ident: str | None = Field(default=None, min_length=2, max_length=12)
    origin: str | None = Field(default=None, min_length=3, max_length=4)
    destination: str | None = Field(default=None, min_length=3, max_length=4)
    departure_date: date

    @model_validator(mode="after")
    def validate_mode(self) -> "FlightStatusLookupCreate":
        if not self.ident and not (self.origin and self.destination):
            raise ValueError("ident or origin and destination are required")
        self.ident = self.ident.replace(" ", "").upper() if self.ident else None
        self.origin = self.origin.upper() if self.origin else None
        self.destination = self.destination.upper() if self.destination else None
        return self
