from pydantic import BaseModel


class SingleResult(BaseModel):
    filename: str
    result: str
