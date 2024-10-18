
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base


Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship("Book", back_populates="publisher")

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    publisher = relationship("Publisher", back_populates="books")
    stocks = relationship("Stock", back_populates="book")

class Shop(Base):
    __tablename__ = 'shops'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    stocks = relationship("Stock", back_populates="shop")

class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    shop_id = Column(Integer, ForeignKey('shops.id'))
    count = Column(Integer, nullable=False)
    book = relationship("Book", back_populates="stocks")
    shop = relationship("Shop", back_populates="stocks")
    sales = relationship("Sale", back_populates="stock")

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'))
    price = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    stock = relationship("Stock", back_populates="sales")


DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_PORT = os.getenv('DB_PORT', '5432')


DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def get_sales_by_publisher(publisher_name):
    publisher = session.query(Publisher).filter(Publisher.name == publisher_name).first()
    if not publisher:
        print(f"Издатель '{publisher_name}' не найден.")
        return

    sales = session.query(Sale).join(Stock).join(Book).join(Publisher).join(Shop)\
        .filter(Publisher.id == publisher.id).all()

    for sale in sales:
        book_title = sale.stock.book.title
        shop_name = sale.stock.shop.name
        price = sale.price
        date = sale.date.strftime("%d-%m-%Y")
        print(f"{book_title} | {shop_name} | {price} | {date}")

if __name__ == "__main__":
    publisher_name = input("Введите имя издателя: ")
    get_sales_by_publisher(publisher_name)
