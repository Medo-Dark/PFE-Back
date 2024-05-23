from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, func, Table, ForeignKey
from sqlalchemy.orm import relationship

from config.database import Base

user_department_association = Table('user_department_association', Base.metadata,
                                Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
                                Column('department_id', Integer, ForeignKey('departments.id', ondelete='CASCADE'))
                                )


user_plant_association = Table('user_plant_association', Base.metadata,
                                Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
                                Column('plant_id', Integer, ForeignKey('plants.id', ondelete='CASCADE'))
                                )


user_team_association = Table('user_team_association',Base.metadata,
                                Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
                                Column('team_id', Integer, ForeignKey('teams.id', ondelete='CASCADE'))
                                )

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(
        Enum('Superviseur', 'Manager', 'Zone leader', 'Admin', name='roles_enum'),
        nullable=False
    )
    account_status = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    departments = relationship("Department", secondary=user_department_association, back_populates="users")
    plants = relationship("Plant", secondary=user_plant_association, back_populates="users")
    teams = relationship("Team", secondary=user_team_association, back_populates="users")


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    users = relationship("User", secondary=user_department_association, back_populates="departments")


class Plant(Base):
    __tablename__ = 'plants'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    users = relationship("User", secondary=user_plant_association, back_populates="plants")


class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    users = relationship("User", secondary=user_team_association, back_populates="teams")
