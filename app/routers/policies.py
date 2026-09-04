from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import (
    admin_required,
    get_current_user,
)
from app.models.policy import Policy
from app.models.customer import Customer
from app.models.user import User

from app.schemas.policy import (
    PolicyCreate,
    PolicyUpdate,
    PolicyResponse,
)

router = APIRouter(
    prefix="/policies",
    tags=["Policies"],
)

@router.post(
    "",
    response_model=PolicyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_policy(
    policy: PolicyCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required),
):

    customer = (
        db.query(Customer)
        .filter(Customer.id == policy.customer_id)
        .first()
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    existing = (
        db.query(Policy)
        .filter(
            Policy.policy_number == policy.policy_number
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Policy number already exists",
        )

    if policy.premium_amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Premium amount must be greater than 0",
        )

    if policy.coverage_amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Coverage amount must be greater than 0",
        )

    if policy.status not in [
        "Active",
        "Expired",
        "Cancelled",
    ]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status",
        )

    new_policy = Policy(
        customer_id=policy.customer_id,
        policy_number=policy.policy_number,
        policy_type=policy.policy_type,
        premium_amount=policy.premium_amount,
        coverage_amount=policy.coverage_amount,
        policy_start_date=policy.policy_start_date,
        policy_end_date=policy.policy_end_date,
        status=policy.status,
    )

    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)

    return new_policy

@router.get(
    "",
    response_model=list[PolicyResponse],
)
def get_policies(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    query = db.query(Policy)

    if current_user.role == "Customer":

        customer = (
            db.query(Customer)
            .filter(
                Customer.user_id == current_user.id
            )
            .first()
        )

        if customer is None:
            return []

        query = query.filter(
            Policy.customer_id == customer.id
        )

    offset = (page - 1) * limit

    return (
        query.offset(offset)
        .limit(limit)
        .all()
    )


@router.get(
    "/search",
    response_model=PolicyResponse,
)
def search_policy(
    policy_number: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    policy = (
        db.query(Policy)
        .filter(Policy.policy_number == policy_number)
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

        if customer is None or policy.customer_id != customer.id:
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

    return policy


@router.get(
    "/{policy_id}",
    response_model=PolicyResponse,
)
def get_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    policy = (
        db.query(Policy)
        .filter(Policy.id == policy_id)
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

        if customer is None or policy.customer_id != customer.id:
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

    return policy


@router.put(
    "/{policy_id}",
    response_model=PolicyResponse,
)
def update_policy(
    policy_id: int,
    policy_data: PolicyUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required),
):
    policy = (
        db.query(Policy)
        .filter(Policy.id == policy_id)
        .first()
    )

    if policy is None:
        raise HTTPException(
            status_code=404,
            detail="Policy not found",
        )

    if policy_data.premium_amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Premium amount must be greater than 0",
        )

    if policy_data.coverage_amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Coverage amount must be greater than 0",
        )

    if policy_data.status not in [
        "Active",
        "Expired",
        "Cancelled",
    ]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status",
        )

    policy.policy_type = policy_data.policy_type
    policy.premium_amount = policy_data.premium_amount
    policy.coverage_amount = policy_data.coverage_amount
    policy.policy_start_date = policy_data.policy_start_date
    policy.policy_end_date = policy_data.policy_end_date
    policy.status = policy_data.status

    db.commit()
    db.refresh(policy)

    return policy

