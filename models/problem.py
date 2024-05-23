from sqlalchemy import Table, Column, Integer, String, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import relationship

from config.database import Base

# Association table for the many-to-many relationship between Problem and Cause
problem_cause_association = Table(
    'problem_cause_association',
    Base.metadata,
    Column('problem_id', Integer, ForeignKey('problems.id', ondelete='CASCADE')),
    Column('cause_id', Integer, ForeignKey('causes.id', ondelete='CASCADE'))
)

# Association table for the many-to-many relationship between Problem and Alert
problem_alert_association = Table(
    'problem_alert_association',
    Base.metadata,
    Column('problem_id', Integer, ForeignKey('problems.id', ondelete='CASCADE')),
    Column('alert_id', Integer, ForeignKey('alerts.id', ondelete='CASCADE'))
)


class Problem(Base):
    __tablename__ = 'problems'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    details = Column(Text, nullable=False)
    how_detected = Column(Text, nullable=False)
    who_detected = Column(String(255), nullable=False)
    where = Column(String(255), nullable=False)
    when = Column(DateTime, nullable=False)
    bad_pieces = Column(Integer, nullable=False)
    qte_tri = Column(Integer, nullable=False)
    qte_nok = Column(Integer, nullable=False)
    reboot_time = Column(DateTime, nullable=True)
    level = Column(String(255), nullable=False, default="Superviseur")
    status = Column(String(255), nullable=False, default="open")
    username = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    causes = relationship("Cause", secondary="problem_cause_association")
    actions = relationship("Action", back_populates="problem")
    attachments = relationship("Attachment", back_populates="problem")
    alerts = relationship("Alert", secondary="problem_alert_association", back_populates="problems")
    checked_by = relationship("CheckedBy", back_populates="problem")

class Cause(Base):
    __tablename__ = 'causes'
    id = Column(Integer, primary_key=True, index=True)
    cause = Column(String(255), nullable=False)
    details = Column(Text, nullable=False)

    problems = relationship("Problem", secondary="problem_cause_association", back_populates="causes")


class Action(Base):
    __tablename__ = 'actions'
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)
    who = Column(String(255), nullable=False)
    problem_id = Column(Integer, ForeignKey('problems.id'))

    problem = relationship("Problem", back_populates="actions")


class Attachment(Base):
    __tablename__ = 'attachments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    problem_id = Column(Integer, ForeignKey('problems.id'))

    problem = relationship("Problem", back_populates="attachments")


class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True, index=True)
    alerted = Column(String(255), nullable=False)

    problems = relationship("Problem", secondary="problem_alert_association", back_populates="alerts")


class CheckedBy(Base):
    __tablename__ = 'checked_by'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    problem_id = Column(Integer, ForeignKey('problems.id'))

    problem = relationship("Problem", back_populates="checked_by")