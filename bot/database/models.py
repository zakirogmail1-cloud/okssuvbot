from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger, Float, Enum, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
import enum


def get_uzbekistan_time():
    from bot.config import get_current_time
    return get_current_time()


class Base(DeclarativeBase):
    pass


class OrderStatus(enum.Enum):
    pending = "pending"
    delivered = "delivered"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    household_size = Column(Integer, nullable=False, default=1)
    language = Column(String(2), nullable=False, default="uz")  # uz, ru, en
    # Saqlangan manzil (birinchi buyurtmada so'raladi, keyingilarda qayta ishlatiladi)
    saved_address = Column(Text, nullable=True)
    saved_lat = Column(Float, nullable=True)
    saved_lng = Column(Float, nullable=True)
    created_at = Column(DateTime, default=get_uzbekistan_time)
    last_reminder_at = Column(DateTime, nullable=True)

    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_number = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)  # jami dona soni (eski moslik uchun)
    items = Column(Text, nullable=True)  # JSON: [{"id","name","qty","price"}]
    total_price = Column(Integer, nullable=True)  # jami summa (so'm)
    address = Column(Text, nullable=False)
    location_lat = Column(Float, nullable=True)
    location_lng = Column(Float, nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    channel_message_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=get_uzbekistan_time)

    user = relationship("User", back_populates="orders")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
