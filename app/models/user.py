from sqlalchemy import Boolean, Column, Integer, String, UniqueConstraint
from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, index=True, nullable=False)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="farmer")
    company_name = Column(String, nullable=True)
    state = Column(String, nullable=True)
    district = Column(String, nullable=True)
    preferred_language = Column(String, nullable=True, default="en")
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint("email", "role", name="uq_user_email_role"),
    )
