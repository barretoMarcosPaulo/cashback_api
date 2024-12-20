import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base


class OrdersModel(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cod = Column(String, index=True)
    status = Column(String, nullable=True)
    amount = Column(Float)
    seller_cpf = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user_id = Column(UUID(as_uuid=True), ForeignKey("users_sellers.id"), nullable=False)

    user = relationship("UserSellerModel", back_populates="orders")

    def __repr__(self):
        return f"<Cod={self.cod} seller={self.seller_cpf}>"
