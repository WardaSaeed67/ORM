from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, and_, or_, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
engine = create_engine("sqlite:///DB.db")
Base = declarative_base()

class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    salary = Column(Integer)

    projects = relationship("Project", back_populates="employee")

class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    project_name = Column(String)
    manager = Column(String)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    employee = relationship("Employee", back_populates="projects")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# ____________insert employee________________


e1 = Employee(id=1, name="Warda Saeed", salary=50000)
e2 = Employee(id=2, name="Mirha ", salary=70000)
e3 = Employee(id=3, name="Kinza", salary=60000)
session.add_all([e1, e2, e3])


# ____________insert project________________


p1 = Project(id=1, project_name="AI System", manager="Boss A", employee=e1)
p2 = Project(id=2, project_name="Web App", manager="Boss B", employee=e2)
p3 = Project(id=3, project_name="Mobile App", manager="Boss C", employee=e3)
session.add_all([p1, p2, p3])
session.commit()


# ____________Filtering________________


print("\n__________Filtering (salary > 55000)__________")
employees = session.query(Employee).filter(Employee.salary > 55000).all()
for e in employees:
    print(e.name, e.salary)


# ____________Ordering________________


print("\n__________Ordering (salary ascending)__________")
employees = session.query(Employee).order_by(Employee.salary).all()
for e in employees:
    print(e.name, e.salary)


# ____________AND Condition________________


print("\n__________AND (salary > 50000 AND name = Ahmed)__________")
employees = session.query(Employee).filter(
    and_(Employee.salary > 50000, Employee.name == "Ahmed")
).all()
for e in employees:
    print(e.name, e.salary)


# ____________OR Condition________________


print("\n__________OR (name = Mirha OR salary > 65000)__________")
employees = session.query(Employee).filter(
    or_(Employee.name == "Mirha", Employee.salary > 65000)
).all()
for e in employees:
    print(e.name, e.salary)


# ____________JOIN________________


print("\n__________JOIN (Employee + Project)__________")
results = session.query(Employee.name, Project.project_name).join(Project).all()
for r in results:
    print(r.name, r.project_name)


# ____________Aggregate Functions________________


print("\n__________Aggregate Functions__________")
count = session.query(func.count(Employee.id)).scalar()
print("Total Employees:", count)
avg_salary = session.query(func.avg(Employee.salary)).scalar()
print("Average Salary:", avg_salary)