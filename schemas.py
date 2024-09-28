from pydantic import BaseModel, Field
from typing import List, Optional


# Схема для элемента заказа (OrderItem)
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    quantity: int = Field(..., ge=1)  # quantity должно быть больше или равно 1


class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True  # Это позволяет Pydantic работать с объектами SQLAlchemy


# Схема для создания заказа (OrderCreate)
class OrderCreate(BaseModel):
    order_items: List[OrderItemCreate]


# Схема для отображения информации о заказе (Order)
class Order(BaseModel):
    id: int
    status: str
    order_items: List[OrderItem]  # Заказ должен включать список элементов заказа
    created_at: Optional[str] = None

    class Config:
        from_attributes = True  # Для поддержки работы с объектами SQLAlchemy


# Схема для товара (Product)
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity_in_stock: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
