from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import (
    declarative_base,
    relationship,
)  # Добавляем relationship для связи моделей
from datetime import datetime

Base = declarative_base()


# Модель товара (Product)
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    quantity_in_stock = Column(Integer, nullable=False)

    # Связь с элементами заказа
    order_items = relationship("OrderItem", back_populates="product")


# Модель заказа (Order)
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="in_process")

    # Связь с элементами заказа
    order_items = relationship("OrderItem", back_populates="order")


# Модель элемента заказа (OrderItem)
class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False)

    # Связь с заказом
    order = relationship("Order", back_populates="order_items")

    # Связь с продуктом
    product = relationship("Product", back_populates="order_items")
