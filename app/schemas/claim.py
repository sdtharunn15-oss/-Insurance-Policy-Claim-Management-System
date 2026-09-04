from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ClaimCreate(BaseModel):
    policy_id: int
    claim_amount: float = Field(gt=0)
    claim_reason: str
    claim_date: date


class ClaimUpdate(BaseModel):
    claim_amount: float = Field(gt=0)
    claim_reason: str
    claim_date: date


class ClaimResponse(BaseModel):
    id: int
    policy_id: int
    claim_amount: float
    claim_reason: str
    claim_date: date
    claim_status: str

    model_config = ConfigDict(from_attributes=True)