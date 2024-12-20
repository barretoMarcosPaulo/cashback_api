from typing import Any, Dict, Optional
from datetime import datetime, timezone

import requests
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.application.dtos import UserSellerCreateDTO, OrderCreateDTO
from app.core.security import hash_password
from app.domain.entities import UserSeller
from app.domain.interfaces import UserRepositoryInterface, CashBackApiInterface
from app.models.order import OrdersModel
from app.models.user import UserSellerModel
from app.core.config import settings


class UserSellerRepository(UserRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> Optional[UserSeller]:
        stmt = select(UserSellerModel).where(UserSellerModel.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_user_by_cpf(self, cpf: str) -> Optional[UserSeller]:
        stmt = select(UserSellerModel).where(UserSellerModel.cpf == cpf)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create_user(self, user: UserSellerCreateDTO):
        hashed_password = hash_password(user.password)
        db_user = UserSellerModel(
            name=user.name, email=user.email, password=hashed_password, cpf=user.cpf
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def get_user_by_filters(
        self, filters: Dict[str, Any]
    ) -> Optional[UserSeller]:
        query = select(UserSellerModel)

        for field, value in filters.items():
            if hasattr(UserSellerModel, field) and value is not None:
                query = query.where(getattr(UserSellerModel, field) == value)

        result = await self.db.execute(query)
        user_model = result.scalars().first()

        if user_model:
            return UserSellerModel(
                id=str(user_model.id),
                name=user_model.name,
                email=user_model.email,
                cpf=user_model.cpf,
            )
        return None

    async def create_order_user(self, order: OrderCreateDTO):
        db_order = OrdersModel(
            cod=order.cod,
            amount=order.amount,
            seller_cpf=order.seller_cpf,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),
            status=order.status,
            user_id=order.user_id,
        )
        self.db.add(db_order)
        await self.db.commit()
        await self.db.refresh(db_order)
        return db_order

    async def get_orders_by_user_id(self, user_id: str):
        stmt = select(OrdersModel).where(OrdersModel.user_id == user_id)
        result = await self.db.execute(stmt)
        orders = result.scalars().all()
        return orders

    async def get_orders_of_current_month(self, user_id: str):
        stmt = select(OrdersModel).where(
            func.date_trunc("month", OrdersModel.created_at)
            == func.date_trunc("month", func.now()),
            OrdersModel.user_id == user_id,
        )

        result = await self.db.execute(stmt)
        orders = result.scalars().all()

        return orders


class OBoticarioCashbackApi(CashBackApiInterface):
    def __init__(self):
        self.base_url = settings.CASHBACK_API
        self.access_token = settings.CASHBACK_API_TOKEN

    async def get_accumulated_cashback(self, cpf: str):
        endpoint = f"{self.base_url}?cpf={cpf}"

        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.get(endpoint, headers=headers)

        if response.ok:
            data = response.json()
            return {"accumulated": data.get("body", {}).get("credit")}
        else:
            response.raise_for_status()
