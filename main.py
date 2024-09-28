from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, Order as OrderModel, Product, OrderItem
from schemas import Order as OrderSchema, OrderCreate
from contextlib import asynccontextmanager
from typing import List


# Lifespan для инициализации приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)  # Создаем все таблицы в базе данных
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Aleksandr Zaretsky warehouse API"}


# Получение сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Эндпоинт для создания нового заказа
@app.post("/orders/", response_model=OrderSchema)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    for item in order.order_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product is None or product.quantity_in_stock < item.quantity:
            raise HTTPException(status_code=400, detail="Product is out of stock")

    db_order = OrderModel(
        status="in_process"
    )  # Инициализируем заказ с статусом по умолчанию
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Создаем элементы заказа и уменьшаем количество на складе
    for item in order.order_items:
        order_item = OrderItem(
            order_id=db_order.id, product_id=item.product_id, quantity=item.quantity
        )
        db.add(order_item)
        product.quantity_in_stock -= item.quantity
        db.add(product)

    db.commit()
    db.refresh(db_order)  # Обновляем объект заказа, чтобы отобразить созданные элементы
    return db_order


# Эндпоинт для получения списка всех заказов
@app.get("/orders/", response_model=List[OrderSchema])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    orders = db.query(OrderModel).offset(skip).limit(limit).all()
    return orders


# Эндпоинт для получения информации о заказе по ID
@app.get("/orders/{order_id}", response_model=OrderSchema)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# Эндпоинт для обновления статуса заказа
@app.patch("/orders/{order_id}/status", response_model=OrderSchema)
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    valid_statuses = ["in_process", "shipped", "delivered", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}"
        )

    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order
