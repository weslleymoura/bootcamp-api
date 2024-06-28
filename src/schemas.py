from pydantic import BaseModel


class ApiCallBase(BaseModel):
    lat: float
    lng: float

    class Config:
        from_attributes = True


class CreateApiCall(ApiCallBase):
    class Config:
        from_attributes = True