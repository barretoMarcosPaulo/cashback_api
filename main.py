from fastapi import FastAPI, Depends
from app.application.dtos import OrderCreateDTO, UserLoginDTO, UserSellerCreateDTO
from app.infrastructure.database import SessionLocal
from app.application.handlers import (
    create_user_seller_handler, 
    user_login_handler, 
    verify_and_extract_jwt_handler,
    create_order_handler,
    get_seller_orders_handle,
    get_accumulated_cashback_handle,
)
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/auth/login")
async def user_login(login: UserLoginDTO, db: AsyncSession = Depends(get_db), ):
    return await user_login_handler(login, db)

@app.post("/sellers")
async def create_user_seller(user_create: UserSellerCreateDTO, db: AsyncSession = Depends(get_db), ):
    return await create_user_seller_handler(user_create, db)

@app.post("/sellers/orders")
async def create_seller_order(
    order: OrderCreateDTO,
    db: AsyncSession = Depends(get_db), 
    current_user: str = Depends(verify_and_extract_jwt_handler)
):
    return await create_order_handler(order=order, user_id=current_user, db=db)

@app.get("/sellers/orders")
async def get_seller_orders(
    db: AsyncSession = Depends(get_db), 
    current_user: str = Depends(verify_and_extract_jwt_handler)
):
    return await get_seller_orders_handle(user_id=current_user, db=db)

@app.get("/sellers/accumulated-cashback")
async def get_accumulated_accumulated(
    cpf: str,
    db: AsyncSession = Depends(get_db), 
    current_user: str = Depends(verify_and_extract_jwt_handler),
):
    return await get_accumulated_cashback_handle(seller_cpf=cpf)

