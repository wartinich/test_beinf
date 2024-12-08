from pydantic import BaseModel


class RecordCreate(BaseModel):
    text: str


class RecordResponse(BaseModel):
    id: int
    link: str
    text: str
    status: str

    class Config:
        orm_mode = True
