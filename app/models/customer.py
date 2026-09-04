from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    name = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    phone = Column(String(20), nullable=False)

    address = Column(String(255), nullable=False)

    user = relationship(
        "User",
        back_populates="customers"
    )

    policies = relationship(
        "Policy",
        back_populates="customer",
        cascade="all, delete-orphan"
    )