from._base import BaseAPIModel


class Quiz(BaseAPIModel):
    pass


class Result(BaseAPIModel):
    name: str
    description: str