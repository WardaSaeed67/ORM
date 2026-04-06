from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

#____________Database connection________________

engine = create_engine("sqlite:///test.db")

#____________base class__________________

Base = declarative_base()

#_____________User table___________________

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

#___________One-to-One relationship_________________

    profile = relationship("Profile", back_populates="user", uselist=False)


#____________Profile table___________

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    bio = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="profile")
Base.metadata.create_all(engine)

#__________Session__________________

Session = sessionmaker(bind=engine)
session = Session()

#__________Inserting data_____________

new_user = User(name="Warda Saeed")
new_profile = Profile(bio="Python Developer")

# __________Link both_____________

new_user.profile = new_profile
session.add(new_user)
session.commit()

#_______Fetch data_________________

user = session.query(User).first()
print(user.name)
print(user.profile.bio)

profile = session.query(Profile).first()
print(profile.user.name)