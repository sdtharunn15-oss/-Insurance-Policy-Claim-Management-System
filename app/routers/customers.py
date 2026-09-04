from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import admin_required
from app.models.user import User
from app.models.customer import Customer
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    customer: CustomerCreate,
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required),
):
    """
    Create a customer profile for an existing user.
    The user must have the Customer role.
    """

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if user.role != "Customer":
        raise HTTPException(
            status_code=400,
            detail="Selected user is not a customer",
        )

    existing_profile = (
        db.query(Customer)
        .filter(Customer.user_id == user_id)
        .first()
    )

    if existing_profile:
        raise HTTPException(
            status_code=400,
            detail="Customer profile already exists",
        )

    existing_email = (
        db.query(Customer)
        .filter(Customer.email == customer.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Customer email already exists",
        )

    new_customer = Customer(
        user_id=user.id,
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address,
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


@router.get(
    "",
    response_model=list[CustomerResponse],
)
def get_customers(
    db: Session = Depends(get_db),
    current_user=Depends(admin_required),
):
    return db.query(Customer).all()


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required),
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return customer


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required),
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    duplicate_email = (
        db.query(Customer)
        .filter(
            Customer.email == customer_data.email,
            Customer.id != customer_id,
        )
        .first()
    )

    if duplicate_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists",
        )

    customer.name = customer_data.name
    customer.email = customer_data.email
    customer.phone = customer_data.phone
    customer.address = customer_data.address

    db.commit()
    db.refresh(customer)

    return customer


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_200_OK,
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required),
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted successfully"
    }