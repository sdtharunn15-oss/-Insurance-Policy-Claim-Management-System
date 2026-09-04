from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class PolicyCreate(BaseModel):
    customer_id: int
    policy_number: str
    policy_type: str
    premium_amount: float = Field(gt=0)
    coverage_amount: float = Field(gt=0)
    policy_start_date: date
    policy_end_date: date
    status: str


class PolicyUpdate(BaseModel):
    policy_type: str
    premium_amount: float = Field(gt=0)
    coverage_amount: float = Field(gt=0)
    policy_start_date: date
    policy_end_date: date
    status: str


class PolicyResponse(BaseModel):
    id: int
    customer_id: int
    policy_number: str
    policy_type: str
    premium_amount: float
    coverage_amount: float
    policy_start_date: date
    policy_end_date: date
    status: str

    model_config = ConfigDict(from_attributes=True)