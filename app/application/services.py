from app.application.dtos import (
    OrderCreateDTO,
    OrderResponseDTO,
    UserLoginDTO,
    UserSellerCreateDTO,
)
from app.core.security import create_access_token, decode_access_token, verify_password
from app.domain.interfaces import UserRepositoryInterface, CashBackApiInterface
from app.domain.entities import UserSeller
from app.domain.exceptions import (
    AuthenticationError,
    UserEmailAlreadyExistsError,
    UserCPFAlreadyExistsError,
    UserNotFoundError,
)
from app.core.config import settings


class JwtAuthService:
    def verify_jwt(self, token_jwt: str):
        return decode_access_token(token_jwt)

    def create_token_jwt(self, additional_data: dict):
        return create_access_token(data=additional_data)


class AccumulatedCashBackService:
    def __init__(self, cashback_api: CashBackApiInterface):
        self.cashback_api = cashback_api

    async def get_cashback(self, cpf):
        return await self.cashback_api.get_accumulated_cashback(cpf=cpf)


class UserSellerService:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def create_user_seller(self, user: UserSellerCreateDTO) -> UserSeller:
        existing_user_email = await self.user_repository.get_user_by_email(user.email)
        if existing_user_email:
            raise UserEmailAlreadyExistsError("User already exists with email.")

        existing_user_cpf = await self.user_repository.get_user_by_cpf(user.cpf)
        if existing_user_cpf:
            raise UserCPFAlreadyExistsError("User already exists cpf.")

        return await self.user_repository.create_user(user)

    async def login_user(self, login_data: UserLoginDTO):
        existing_user_email = await self.user_repository.get_user_by_email(
            login_data.email
        )
        if not existing_user_email:
            raise AuthenticationError

        if not verify_password(login_data.password, existing_user_email.password):
            raise AuthenticationError

        jwt_token_payload = {"user_id": str(existing_user_email.id)}

        token = JwtAuthService().create_token_jwt(additional_data=jwt_token_payload)
        return {"access_token": token}

    async def create_order_user_seller(self, order: OrderCreateDTO, user_id: str):
        filters = {"id": user_id, "cpf": order.seller_cpf}
        existing_user = await self.user_repository.get_user_by_filters(filters)

        if not existing_user:
            raise UserNotFoundError("Seller not found.")

        if order.seller_cpf == settings.MANAGER_CPF:
            order.status = "Aprovado"

        order.user_id = user_id
        return await self.user_repository.create_order_user(order)

    async def get_seller_orders(self, user_id: str):
        existing_user = await self.user_repository.get_user_by_filters({"id": user_id})
        if not existing_user:
            raise UserNotFoundError("Seller not found.")

        orders = await self.user_repository.get_orders_of_current_month(user_id=user_id)

        total_orders_amount = round(sum(order.amount for order in orders), 2)

        percentage_cashback = 0.10
        if total_orders_amount <= 1500:
            percentage_cashback = 0.15
        else:
            percentage_cashback = 0.20

        response = []
        for order in orders:
            order_response = OrderResponseDTO(
                id=str(order.id),
                amount=order.amount,
                cod=order.cod,
                created_at=order.created_at,
                seller_cpf=order.seller_cpf,
                status=order.status,
                cashback_percentage=percentage_cashback,
                user_id=str(order.user_id),
            )
            order_response.calculate_cashback()
            response.append(order_response)
        return response
