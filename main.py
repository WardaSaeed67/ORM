from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# ____________database create__________________
engine = create_engine("sqlite:///college.db")
Base = declarative_base()

# ______________Student Table_________________

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


#_____________Course Table______________

class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)
    course_name = Column(String)
    teacher = Column(String)


# _______________tables create______________
Base.metadata.create_all(engine)


# ______________session create_______________
Session = sessionmaker(bind=engine)
session = Session()


# _____________insert student__________________
s1 = Student(id=1, name="Warda", age=20)
s2 = Student(id=2, name="Sara", age=22)
session.add(s1)
session.add(s2)


# ______________insert course____________________
c1 = Course(id=1, course_name="SDA", teacher="Sir A")
c2 = Course(id=2, course_name="SRE", teacher="Sir B")
session.add(c1)
session.add(c2)
session.commit()


# _______________read students_______________
students = session.query(Student).all()
print("Students:")
for s in students:
    print(s.id, s.name, s.age)


# _________________read courses_________________
courses = session.query(Course).all()
print("Courses:")
for c in courses:
    print(c.id, c.course_name, c.teacher)