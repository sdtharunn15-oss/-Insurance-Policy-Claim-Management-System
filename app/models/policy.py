from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False
    )

    policy_number = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    policy_type = Column(String(100), nullable=False)

    premium_amount = Column(Float, nullable=False)

    coverage_amount = Column(Float, nullable=False)

    policy_start_date = Column(Date, nullable=False)

    policy_end_date = Column(Date, nullable=False)

    status = Column(String(30), nullable=False)

    customer = relationship(
        "Customer",
        back_populates="policies"
    )

    claims = relationship(
        "Claim",
        back_populates="policy",
        cascade="all, delete-orphan"
    )