from sqlalchemy import Column, String, JSON
from app.database.database import Base


class GovernmentScheme(Base):
    __tablename__ = "government_schemes"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    eligibility = Column(String, nullable=True)
    description = Column(String, nullable=True)
    benefits = Column(JSON, default=list)
    link = Column(String, nullable=True)
    crops = Column(JSON, default=list)
