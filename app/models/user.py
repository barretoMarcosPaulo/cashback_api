import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database import Base


class UserSellerModel(Base):
    __tablename__ = "users_sellers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)

    orders = relationship("OrdersModel", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} name={self.name} email={self.email}>"
