from pydantic import BaseModel


class PagintaionSchema(BaseModel):
    search: str
    offset: int
    limit: int
