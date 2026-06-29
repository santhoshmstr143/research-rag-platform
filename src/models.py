from pydantic import BaseModel


class QueryRequest(BaseModel):

    question: str

    papers: list[str] = []