from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import (
    get_current_user,
    admin_required,
    agent_required,
)

from app.models.claim import Claim
from app.models.policy import Policy
from app.models.customer import Customer

from app.schemas.claim import (
    ClaimCreate,
    ClaimUpdate,
    ClaimResponse,
)

router = APIRouter(
    prefix="/claims",
    tags=["Claims"],
)

@router.post(
    "",
    response_model=ClaimResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_claim(
    claim: ClaimCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    policy = (
        db.query(Policy)
        .filter(Policy.id == claim.policy_id)
        .first()
    )

    if policy is None:
        raise HTTPException(
            status_code=404,
            detail="Policy not found",
        )

    if current_user.role == "Customer":

        customer = (
            db.query(Customer)
            .filter(Customer.user_id == current_user.id)
            .first()
        )

        if customer is None or customer.id != policy.customer_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

    if policy.status != "Active":
        raise HTTPException(
            status_code=400,
            detail="Claims can only be raised for active policies",
        )

    if claim.claim_amount > policy.coverage_amount:
        raise HTTPException(
            status_code=400,
            detail="Claim amount exceeds policy coverage",
        )

    new_claim = Claim(
        policy_id=claim.policy_id,
        claim_amount=claim.claim_amount,
        claim_reason=claim.claim_reason,
        claim_date=claim.claim_date,
        claim_status="Submitted",
    )

    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)

    return new_claim


@router.get(
    "",
    response_model=list[ClaimResponse],
)
def get_claims(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    query = db.query(Claim)

    if current_user.role == "Customer":

        customer = (
            db.query(Customer)
            .filter(Customer.user_id == current_user.id)
            .first()
        )

        if customer is None:
            return []

        policy_ids = [
            p.id
            for p in customer.policies
        ]

        query = query.filter(
            Claim.policy_id.in_(policy_ids)
        )

    return (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )



@router.get(
    "/{claim_id}",
    response_model=ClaimResponse,
)
def get_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    claim = (
        db.query(Claim)
        .filter(Claim.id == claim_id)
        .first()
    )

    if claim is None:
        raise HTTPException(
            status_code=404,
            detail="Claim not found",
        )

    if current_user.role == "Customer":
        customer = (
            db.query(Customer)
            .filter(Customer.user_id == current_user.id)
            .first()
        )

        policy = (
            db.query(Policy)
            .filter(Policy.id == claim.policy_id)
            .first()
        )

        if (
            customer is None
            or policy is None
            or policy.customer_id != customer.id
        ):
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

    return claim


@router.put(
    "/{claim_id}",
    response_model=ClaimResponse,
)
def update_claim(
    claim_id: int,
    claim_data: ClaimUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    claim = (
        db.query(Claim)
        .filter(Claim.id == claim_id)
        .first()
    )

    if claim is None:
        raise HTTPException(
            status_code=404,
            detail="Claim not found",
        )

    if claim.claim_status in ["Approved", "Rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Approved or rejected claims cannot be modified",
        )

    policy = (
        db.query(Policy)
        .filter(Policy.id == claim.policy_id)
        .first()
    )

    if current_user.role == "Customer":
        customer = (
            db.query(Customer)
            .filter(Customer.user_id == current_user.id)
            .first()
        )

        if (
            customer is None
            or policy.customer_id != customer.id
        ):
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

    if claim_data.claim_amount > policy.coverage_amount:
        raise HTTPException(
            status_code=400,
            detail="Claim amount exceeds policy coverage",
        )

    claim.claim_amount = claim_data.claim_amount
    claim.claim_reason = claim_data.claim_reason
    claim.claim_date = claim_data.claim_date

    db.commit()
    db.refresh(claim)

    return claim


@router.get(
    "/status/filter",
    response_model=list[ClaimResponse],
)
def filter_claims(
    status: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = (
        db.query(Claim)
        .filter(Claim.claim_status == status)
    )

    if current_user.role == "Customer":
        customer = (
            db.query(Customer)
            .filter(Customer.user_id == current_user.id)
            .first()
        )

        if customer is None:
            return []

        policy_ids = [p.id for p in customer.policies]

        query = query.filter(
            Claim.policy_id.in_(policy_ids)
        )

    return (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

@router.post(
    "/{claim_id}/verify",
)
def verify_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(agent_required),
):

    claim = (
        db.query(Claim)
        .filter(Claim.id == claim_id)
        .first()
    )

    if claim is None:
        raise HTTPException(
            status_code=404,
            detail="Claim not found",
        )

    if claim.claim_status != "Submitted":
        raise HTTPException(
            status_code=400,
            detail="Only submitted claims can be verified",
        )

    claim.claim_status = "Under Review"

    db.commit()
    db.refresh(claim)

    return {
        "message": "Claim verified successfully",
        "claim": claim,
    }


@router.post(
    "/{claim_id}/approve",
)
def approve_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(agent_required),
):

    claim = (
        db.query(Claim)
        .filter(Claim.id == claim_id)
        .first()
    )

    if claim is None:
        raise HTTPException(
            status_code=404,
            detail="Claim not found",
        )

    if claim.claim_status != "Under Review":
        raise HTTPException(
            status_code=400,
            detail="Claim must be under review before approval",
        )

    claim.claim_status = "Approved"

    db.commit()
    db.refresh(claim)

    return {
        "message": "Claim approved successfully",
        "claim": claim,
    }


@router.post(
    "/{claim_id}/reject",
)
def reject_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(agent_required),
):

    claim = (
        db.query(Claim)
        .filter(Claim.id == claim_id)
        .first()
    )

    if claim is None:
        raise HTTPException(
            status_code=404,
            detail="Claim not found",
        )

    if claim.claim_status != "Under Review":
        raise HTTPException(
            status_code=400,
            detail="Claim must be under review before rejection",
        )

    claim.claim_status = "Rejected"

    db.commit()
    db.refresh(claim)

    return {
        "message": "Claim rejected successfully",
        "claim": claim,
    }