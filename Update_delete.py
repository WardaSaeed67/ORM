from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# ____________Database ________________

engine = create_engine("sqlite:///college_updated.db")
Base = declarative_base()

# __________tables_________________

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    # _______relation_____________

    courses = relationship("Course", back_populates="student")

class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)
    course_name = Column(String)
    teacher = Column(String)

#________foreign key___________________________

    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship("Student", back_populates="courses")


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# ________insert__________________
s1 = Student(id=1, name="warda", age=20)
s2 = Student(id=2, name="Ahmed", age=22)
session.add_all([s1, s2])

c1 = Course(id=1, course_name="DB", teacher="Sir A", student=s1)
c2 = Course(id=2, course_name="SRE", teacher="Sir B", student=s1)
c3 = Course(id=3, course_name="Python", teacher="Sir C", student=s2)
c4 = Course(id=4, course_name="AI", teacher="Sir D", student=s2)
session.add_all([c1, c2, c3, c4])
session.commit()

# _____________-update_____________
ali = session.query(Student).filter_by(name="warda").first()
ali.age = 21
session.commit()

#_________________delete__________________
course_to_delete = session.query(Course).filter_by(course_name="AI").first()
session.delete(course_to_delete)
session.commit()

#_________________Relations____________
students = session.query(Student).all()
for s in students:
    print(f"Student: {s.name}, Age: {s.age}")
    for c in s.courses:
        print(f"  Course: {c.course_name}, Teacher: {c.teacher}")