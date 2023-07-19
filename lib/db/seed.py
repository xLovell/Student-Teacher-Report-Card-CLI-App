#!/usr/bin/env python3

from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Student, Teacher, Report_card

if __name__ == "__main__":
    engine = create_engine("sqlite:///report_cards.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Student).delete()
    session.query(Teacher).delete()
    session.query(Report_card).delete()

    faker = Faker()

    courses = ["Math", "Science", "English", "History", "Spanish"]

    students = []

    for _ in range(50):
        student = Student(
            name = f"{faker.first_name()} {faker.last_name()}"
        )

        session.add(student)
        session.commit()

        students.append(student)

    teachers = []

    for _ in range(20):
        teacher = Teacher(
            name = f"{faker.first_name()} {faker.last_name()}",
            course = random.choice(courses)
        )

        session.add(teacher)
        session.commit()

        teachers.append(teacher)

    
    feedbacks = ["Amazing student!", "Great job!", "Need a bit more focus but still good job!", "Need to work on getting assignments in on time.", "Missed too many days for me to be able to pass"]

    for _ in range(300):
        feedback = random.choice(feedbacks)
        if feedback == feedbacks[0]:
            grade = "A"
        elif feedback == feedbacks[1]:
            grade = "B"
        elif feedback == feedbacks[2]:
            grade = "C"
        elif feedback == feedbacks[3]:
            grade = "D"
        elif feedback == feedbacks[4]:
            grade = "F"

        teacher = random.choice(teachers)

        report_card = Report_card(
            student_id = random.choice(students).id,
            teacher_id = teacher.id,
            course = teacher.course,
            feedback = feedback,
            grade = grade
        )
        
        session.add(report_card)
        session.commit()
