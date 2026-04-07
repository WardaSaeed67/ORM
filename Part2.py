from sqlalchemy import create_engine, Column, Integer, String, func, and_, or_
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///test.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    city = Column(String)

Base.metadata.create_all(engine)

students_data = [
    Student(name="Ali", age=20, city="Lahore"),
    Student(name="Sara", age=22, city="Karachi"),
    Student(name="Ahmed", age=20, city="Lahore"),
    Student(name="Ayesha", age=23, city="Islamabad"),
    Student(name="Bilal", age=22, city="Karachi"),
]

session.add_all(students_data)
session.commit()


# ____________FILTER_BY___________
result = session.query(Student).filter_by(city="Karachi").all()
for s in result:
    print(s.name, s.city)



result = session.query(Student).filter(Student.age > 20).all()
for s in result:
    print(s.name, s.age)


result = session.query(Student).filter(
    and_(Student.age > 20, Student.city == "Karachi")
).all()
for s in result:
    print(s.name, s.age, s.city)



result = session.query(Student).filter(
    or_(Student.city == "Lahore", Student.age == 23)
).all()
for s in result:
    print(s.name, s.city, s.age)


# _____________ GROUP BY_______________

result = session.query(
    Student.city,
    func.count(Student.id)
).group_by(Student.city).all()

for city, count in result:
    print(city, count)


# ____________ ORDER BY___________________

result = session.query(Student).order_by(Student.age.desc()).all()
for s in result:
    print(s.name, s.age)


# __________ AGGREGATE FUNCTIONS______________

total_students = session.query(func.count(Student.id)).scalar()
avg_age = session.query(func.avg(Student.age)).scalar()
max_age = session.query(func.max(Student.age)).scalar()
min_age = session.query(func.min(Student.age)).scalar()

print("Total:", total_students)
print("Average Age:", avg_age)
print("Max Age:", max_age)
print("Min Age:", min_age)