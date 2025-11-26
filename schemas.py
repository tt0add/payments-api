from pydantic import BaseModel


class MoneyOperation(BaseModel):
    user_id: int
    sum: int


class TransferOperation(BaseModel):
    user1_id: int
    user2_id: int
    sum: int
