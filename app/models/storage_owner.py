from sqlalchemy import Column, String, ForeignKey
from app.database.database import Base


class StorageOwner(Base):
    __tablename__ = "storage_owners"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    organization = Column(String, nullable=True)
    address = Column(String, nullable=True)
