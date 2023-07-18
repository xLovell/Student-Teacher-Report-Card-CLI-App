from db.models import Student, Teacher, Report_card

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from prettytable import PrettyTable
import time

engine = create_engine('sqlite:///db/report_cards.db')
Session = sessionmaker(bind=engine)
session = Session()

def main_menu():
    print("")
    print("")
    print("")
    print('''
          Hello! Check your report cards below!
          -------------------------------------
          ''')
    print("")

    try:
        purpose = int(input('''
        Please select who you are:
        1 - Student
        2 - Teacher
        0 - Quit program
        
        Enter: '''))
        if purpose == 1:
            student_login()
        elif purpose == 2:
            teacher_login()
        elif purpose == 0:
            print("Bye! Thanks for using my app!")
        else:
            print("Invalid selection. Please input one of the options above")
            time.sleep(3)
            main_menu()
    except ValueError:
        print("Invalid selection. Please input one of the options above")
        time.sleep(3)
        main_menu()


def student_login():
    student_name = str(input("Enter your name or type 'QUIT' to exit: "))
    student = session.query(Student).filter_by(name=student_name.title()).first()
    if student:
        student_report_card(student)
    elif student_name == "QUIT":
        print("Bye! Thanks for using my app!")
    else:
        print("No student found - Plese re-enter name.")
        student_login()

def teacher_login():
    print("teacher login")


def student_report_card(student):
    student_report_cards = session.query(Report_card).filter_by(student_id=student.id).all()
    if student_report_cards:
        print("")
        report_card_table(student_report_cards)
        print("")
    else:
        print("You have no report cards yet!")

def report_card_table(report_cards):
    table = PrettyTable()
    table.title = " REPORT CARDS "
    table.field_names = ["Student Name", "Teacher Name", "Course", "Grade", "Feedback"]
    for report_card in report_cards:
        student = session.query(Student).filter_by(id = report_card.student_id).first()
        teacher = session.query(Teacher).filter_by(id = report_card.teacher_id).first()
        table.add_row([
            student.name,
            teacher.name,
            report_card.course,
            report_card.grade,
            report_card.feedback
        ])
    print(table)