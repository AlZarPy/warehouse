import pytest
from pydantic import ValidationError
from schemas import (
    OrderItemCreate,
    OrderItem,
    OrderCreate,
    Order,
    ProductCreate,
    Product,
)


# Тесты для OrderItemCreate
def test_order_item_create_valid():
    order_item = OrderItemCreate(product_id=1, quantity=2)
    assert order_item.product_id == 1
    assert order_item.quantity == 2


def test_order_item_create_invalid_quantity():
    with pytest.raises(ValidationError) as excinfo:
        OrderItemCreate(product_id=1, quantity=0)  # Invalid quantity
    assert "Input should be greater than or equal to 1" in str(excinfo.value)


# Тесты для OrderCreate
def test_order_create_valid():
    order_create = OrderCreate(order_items=[OrderItemCreate(product_id=1, quantity=2)])
    assert len(order_create.order_items) == 1
    assert order_create.order_items[0].product_id == 1
    assert order_create.order_items[0].quantity == 2


# Тесты для Order
def test_order_valid():
    order = Order(
        id=1,
        status="in_process",
        order_items=[OrderItem(id=1, order_id=1, product_id=1, quantity=2)],
    )
    assert order.id == 1
    assert order.status == "in_process"
    assert len(order.order_items) == 1
    assert order.order_items[0].product_id == 1


# Тесты для ProductCreate
def test_product_create_valid():
    product_create = ProductCreate(
        name="Test Product",
        description="A product for testing",
        price=10.0,
        quantity_in_stock=100,
    )
    assert product_create.name == "Test Product"
    assert product_create.price == 10.0
    assert product_create.quantity_in_stock == 100


# Тесты для Product
def test_product_valid():
    product = Product(
        id=1,
        name="Test Product",
        description="A product for testing",
        price=10.0,
        quantity_in_stock=100,
    )
    assert product.id == 1
    assert product.name == "Test Product"
    assert product.price == 10.0
    assert product.quantity_in_stock == 100
