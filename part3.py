from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# ___________Association table__________
customer_product = Table(
    'customer_product',
    Base.metadata,
    Column('customer_id', Integer, ForeignKey('customers.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)


#____________________MANY TO MANY RELATIONSHIP____________________

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    products = relationship("Product", secondary=customer_product, back_populates="customers")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    customers = relationship("Customer", secondary=customer_product, back_populates="products")


#____________________CASCADE DELETE____________________

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer_name = Column(String)

    items = relationship("OrderItem", cascade="all, delete", back_populates="order")


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    order_id = Column(Integer, ForeignKey('orders.id'))

    order = relationship("Order", back_populates="items")



engine = create_engine("sqlite:///test.db", echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


#____________________APPEND()____________________

customer1 = Customer(name="Ali")
product1 = Product(name="Laptop")

customer1.products.append(product1)

session.add(customer1)
session.commit()


#____________________EXTEND()___________________

product2 = Product(name="Mobile")
product3 = Product(name="Headphones")

customer1.products.extend([product2, product3])

session.commit()


#____________________INNER JOIN___________________

inner_join = session.query(Customer).join(Customer.products).all()

for c in inner_join:
    print("INNER:", c.name)


#____________________LEFT OUTER JOIN____________________

left_join = session.query(Customer).outerjoin(Customer.products).all()

for c in left_join:
    print("LEFT:", c.name)


#___________________RIGHT JOIN____________________

right_join = session.query(Product).outerjoin(Product.customers).all()

for p in right_join:
    print("RIGHT:", p.name)


#____________________FULL OUTER JOIN____________________

left = session.query(Customer).outerjoin(Customer.products).all()
right = session.query(Product).outerjoin(Product.customers).all()

print("FULL JOIN SIMULATION DONE")


#____________________CASCADE DELETE____________________

order1 = Order(customer_name="Ahmed")
item1 = OrderItem(product_name="Laptop")
item2 = OrderItem(product_name="Mouse")

order1.items.append(item1)
order1.items.append(item2)

session.add(order1)
session.commit()

# Delete order → items auto deleted
session.delete(order1)
session.commit()


#____________________CHAINING____________________

result = (
    session.query(Customer)
    .join(Customer.products)   
    .filter(Product.name == "Laptop")
    .order_by(Customer.name)
    .all()
)

for r in result:
    print("CHAIN:", r.name)


