from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import (
    admin_required,
    get_current_user,
)

from app.models.customer import Customer
from app.models.policy import Policy
from app.models.claim import Claim

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)

@router.get("/policies/search")
def search_policy(
    policy_number: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    policy = (
        db.query(Policy)
        .filter(
            Policy.policy_number == policy_number
        )
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
            .filter(
                Customer.user_id == current_user.id
            )
            .first()
        )

        if customer is None:
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

        if policy.customer_id != customer.id:
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

    return policy


@router.get("/claims/status")
def filter_claims(
    status: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    query = (
        db.query(Claim)
        .filter(
            Claim.claim_status == status
        )
    )

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

        policy_ids = [
            p.id for p in customer.policies
        ]

        query = query.filter(
            Claim.policy_id.in_(policy_ids)
        )

    return (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )


@router.get("/customers/{customer_id}/claims")
def customer_claim_history(
    customer_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    # Customers can view only their own history
    if current_user.role == "Customer":
        if customer.user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

    policies = (
        db.query(Policy)
        .filter(Policy.customer_id == customer.id)
        .all()
    )

    if not policies:
        return {
            "customer_id": customer.id,
            "customer_name": customer.name,
            "total_claims": 0,
            "claims": [],
        }

    policy_ids = [policy.id for policy in policies]

    claims = (
        db.query(Claim)
        .filter(Claim.policy_id.in_(policy_ids))
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "customer_id": customer.id,
        "customer_name": customer.name,
        "total_claims": len(claims),
        "claims": claims,
    }


@router.get("/summary")
def report_summary(
    db: Session = Depends(get_db),
    current_user=Depends(admin_required),
):
    total_customers = db.query(Customer).count()
    total_policies = db.query(Policy).count()
    total_claims = db.query(Claim).count()

    active_policies = (
        db.query(Policy)
        .filter(Policy.status == "Active")
        .count()
    )

    approved_claims = (
        db.query(Claim)
        .filter(Claim.claim_status == "Approved")
        .count()
    )

    rejected_claims = (
        db.query(Claim)
        .filter(Claim.claim_status == "Rejected")
        .count()
    )

    under_review_claims = (
        db.query(Claim)
        .filter(Claim.claim_status == "Under Review")
        .count()
    )

    submitted_claims = (
        db.query(Claim)
        .filter(Claim.claim_status == "Submitted")
        .count()
    )

    return {
        "total_customers": total_customers,
        "total_policies": total_policies,
        "active_policies": active_policies,
        "total_claims": total_claims,
        "submitted_claims": submitted_claims,
        "under_review_claims": under_review_claims,
        "approved_claims": approved_claims,
        "rejected_claims": rejected_claims,
    }