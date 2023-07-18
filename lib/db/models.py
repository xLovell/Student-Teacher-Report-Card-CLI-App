from sqlalchemy import (PrimaryKeyConstraint, Column, String, Integer, ForeignKey)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///report_cards.db')

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    __table_args__ = (PrimaryKeyConstraint('id'),)
    
    id = Column(Integer(), primary_key=True)
    name = Column(String())

    def __repr__(self):
        return f"ID: {self.id}, " \
            + f"Name: {self.name} "
    

class Teacher(Base):
    __tablename__ = "teachers"
    __table_args__ = (PrimaryKeyConstraint('id'),)
    
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    course = Column(String())

    def __repr__(self):
        return f"ID: {self.id}, " \
            + f"Name: {self.name}, " \
            + f"Course: {self.course}"
    
class Report_card(Base):
    __tablename__ = "report cards"
    __table_args__ = (PrimaryKeyConstraint('id'),)

    id = Column(Integer(), primary_key=True)
    student_id = Column(Integer(), ForeignKey('students.id'))
    teacher_id = Column(Integer(), ForeignKey('teachers.id'))
    course = Column(String())
    feedback = Column(String())
    grade = Column(String())

    student = relationship('Student', backref=backref("students.id"))
    teacher = relationship('Teacher', backref=backref("teachers.id"))

    def __repr__(self):
        return f"ID: {self.id}, " \
            + f"Student_ID:{self.student_id}, " \
            + f"Teacher_ID:{self.teacher_id}, " \
            + f"Course: {self.course}, "\
            + f"Feedback: {self.feedback}, "\
            + f"Grade: {self.grade} "