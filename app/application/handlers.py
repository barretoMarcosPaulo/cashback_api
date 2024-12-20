import jwt

from fastapi import Depends, HTTPException, status, Request
from app.infrastructure.database import get_db
from app.application.services import (
    JwtAuthService,
    UserSellerService,
    AccumulatedCashBackService,
)
from app.application.dtos import (
    OrderCreateDTO,
    OrderResponseDTO,
    UserLoginDTO,
    UserSellerCreateDTO,
    UserSellerResponseDTO,
)
from app.domain.exceptions import (
    AuthenticationError,
    UserEmailAlreadyExistsError,
    UserCPFAlreadyExistsError,
    UserNotFoundError,
)
from app.infrastructure.repositories import UserSellerRepository, OBoticarioCashbackApi
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user_seller_handler(
    user_seller_create: UserSellerCreateDTO,
    db: AsyncSession,
) -> UserSellerResponseDTO:
    service = UserSellerService(UserSellerRepository(db))

    try:
        user = await service.create_user_seller(user_seller_create)
        return UserSellerResponseDTO(
            email=user.email, id=str(user.id), name=user.name, cpf=user.cpf
        )

    except UserEmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User already exists with email {user_seller_create.email}.",
        )

    except UserCPFAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User already exists with cpf {user_seller_create.cpf}.",
        )


async def user_login_handler(
    login_data: UserLoginDTO,
    db: AsyncSession,
) -> str:

    service = UserSellerService(UserSellerRepository(db))
    try:
        token = await service.login_user(login_data)
        return token

    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )


async def verify_and_extract_jwt_handler(request: Request) -> str:

    try:
        service = JwtAuthService()
        user_token = request.headers.get("Authorization")
        if not user_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header not found.",
            )
        data = service.verify_jwt(token_jwt=user_token)
        return data.get("user_id")

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired.",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid.",
        )


async def create_order_handler(
    order: OrderCreateDTO,
    user_id: str,
    db: AsyncSession,
) -> OrderResponseDTO:
    service = UserSellerService(UserSellerRepository(db))

    try:
        return await service.create_order_user_seller(order=order, user_id=user_id)

    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


async def get_seller_orders_handle(
    user_id: str,
    db: AsyncSession,
) -> OrderResponseDTO:
    service = UserSellerService(UserSellerRepository(db))

    try:
        return await service.get_seller_orders(user_id=user_id)

    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


async def get_accumulated_cashback_handle(seller_cpf:str) -> OrderResponseDTO:
    service = AccumulatedCashBackService(OBoticarioCashbackApi())
    return await service.get_cashback(seller_cpf)

