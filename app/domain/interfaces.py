from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session

from app.application.dtos import OrderCreateDTO, UserSellerCreateDTO
from app.domain.entities import UserSeller


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def create_user(self, user: UserSellerCreateDTO) -> UserSeller:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[UserSeller]:
        pass

    @abstractmethod
    async def get_user_by_cpf(self, cpf: str) -> Optional[UserSeller]:
        pass

    @abstractmethod
    async def get_user_by_filters(self, filters: dict) -> Optional[UserSeller]:
        pass

    @abstractmethod
    async def create_order_user(self, order: OrderCreateDTO) -> Optional[UserSeller]:
        pass

    @abstractmethod
    async def get_orders_by_user_id(self, user_id: str):
        pass

    @abstractmethod
    async def get_orders_of_current_month(self, user_id: str):
        pass


class CashBackApiInterface(ABC):
    @abstractmethod
    async def get_accumulated_cashback(self, cpf: str):
        pass
