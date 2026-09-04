from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)

    policy_id = Column(
        Integer,
        ForeignKey("policies.id", ondelete="CASCADE"),
        nullable=False
    )

    claim_amount = Column(Float, nullable=False)

    claim_reason = Column(String(500), nullable=False)

    claim_date = Column(Date, nullable=False)

    claim_status = Column(
        String(30),
        default="Submitted",
        nullable=False
    )

    policy = relationship(
        "Policy",
        back_populates="claims"
    )