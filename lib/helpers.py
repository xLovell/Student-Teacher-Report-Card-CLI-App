from db.models import Student, Teacher, Report_card

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from prettytable import PrettyTable
import time

engine = create_engine('sqlite:///db/report_cards.db')
Session = sessionmaker(bind=engine)
session = Session()

YES = ["yes", "YES", "y", "Y"]
NO = ["no", "NO", "n", "N"]

def main_menu():
    print("")
    print("")
    print('''
          Hello! Check your report cards below!
          -------------------------------------
          ''')
    print("")

    # try:
    purpose = int(input('''
        Please select who you are:
        1 - Student
        2 - Teacher
        0 - Quit program
        
        Enter: '''))
    print("")
    if purpose == 1:
        student_login()
    elif purpose == 2:
        teacher_login()
    elif purpose == 0:
        print("Bye! Thanks for using my app!")
    else:
        print("Invalid selection. Please input one of the options above")
        time.sleep(2)
        main_menu()
    # except ValueError:
    #     print("Invalid selection. Please input one of the options above")
    #     time.sleep(3)
    #     main_menu()


def student_login():
    student_name = str(input("Enter your name or type 'QUIT' to exit: "))
    student = session.query(Student).filter_by(name=student_name.title()).first()
    if student:
        student_report_card(student)
    elif student_name == "QUIT":
        print("Bye! Thanks for using my app!")
    else:
        print("No student found - Please re-enter name.")
        student_login()

def teacher_login():
    teacher_name = str(input("Enter your name or type 'QUIT' to exit: "))
    teacher = session.query(Teacher).filter_by(name=teacher_name.title()).first()
    if teacher:
        teacher_menu(teacher)
    elif teacher_name == "QUIT":
        print("Bye! Thanks for using my app!")
    else:
        print("No teacher found - Please re-enter name.")
        teacher_login()
    

def student_report_card(student):
    student_report_cards = session.query(Report_card).filter_by(student_id=student.id).all()
    if student_report_cards:
        print("")
        student_report_card_table(student_report_cards)
        print("")
    else:
        print("You have no report cards yet!")

def teacher_menu(teacher):

    # try:
        option = int(input('''
        What would you like to do?
        1 - View all your report cards
        2 - Edit a report card
        3 - Delete a report card
        4 - Create new report card
        0 - Quit program
                           
        Enter: '''))

        if option == 1:
            teacher_report_cards(teacher)
        elif option == 2:
            teacher_report_cards_edit(teacher)
        elif option == 3:
            teacher_report_cards_delete(teacher)
        elif option == 4:
            teacher_new_report_card(teacher)
        elif option == 0:
            print("Bye! Thanks for using my app!")
        else:
            print("Invalid selection. Please input one of the options above")
            time.sleep(2)
            teacher_menu(teacher)
    # except ValueError:
    #     print("Invalid selection. Please input one of the options above")
    #     time.sleep(3)
    #     teacher_menu(teacher)
    

def teacher_report_cards(teacher):
    teacher_report_list = session.query(Report_card).filter_by(teacher_id=teacher.id).all()
    if teacher_report_list:
        print("")
        print(teacher_report_card_table(teacher_report_list))
        print("")
        time.sleep(2)
        teacher_menu(teacher)
    else:
        print("You have not yet created any report cards.")
        print("")
        time.sleep(2)
        teacher_menu(teacher)

def teacher_report_cards_edit(teacher):
    teacher_report_list = session.query(Report_card).filter_by(teacher_id=teacher.id).all()
    if teacher_report_list:
        print("")
        print(teacher_report_card_table(teacher_report_list))
        print("")
        report_id = input("Please enter the id of the report card to edit: ")
        report_card = session.query(Report_card).filter_by(id = report_id).first()
        if report_card and report_card.teacher_id == teacher.id:
            edit = int(input('''
        What would you like to edit?
        1 - Grade
        2 - Feedback
        0 - Quit program
        
        Enter: '''))
            print("")
            if edit == 1:
                edit_grade(report_card, teacher)
            elif edit == 2:
                edit_feedback(report_card, teacher)
            elif edit == 0:
                print("Bye! Thanks for using my app!")
            else:
                print("Invalid input - Please retry")
                teacher_report_cards_edit(teacher)
        else:
            print("Invalid report card ID")
            time.sleep(2)
            teacher_report_cards_edit(teacher)
    else:
        print("You have not yet created any report cards.")
        time.sleep(2)
        main_menu()

def edit_grade(report_card, teacher):
    previous_grade = report_card.grade
    grades = ["A", "a", "B", "b", "C", "c", "D", "d", "F", "f"]
    new_grade = input("Enter new grade: ")
    if new_grade in grades:
        report_card.grade = new_grade
        session.commit()
        print(f"Updated grade from {previous_grade} to {new_grade}")
        time.sleep(1)
        teacher_menu(teacher)
    else:
        print("Invalid grade - Please re-enter")
        edit_grade(report_card)


def edit_feedback(report_card, teacher):
    new_feedback = input(str("Enter new feedback: "))
    if new_feedback:
        report_card.feedback = new_feedback
        session.commit()
        print(f'Updated feedback to: "{new_feedback}"')
        time.sleep(1)
        teacher_menu(teacher)
    else:
        print("Invalid input - Please re-enter")
        edit_feedback(report_card)

def teacher_report_cards_delete(teacher):
    teacher_report_list = session.query(Report_card).filter_by(teacher_id=teacher.id).all()
    if teacher_report_list:
        print("")
        print(teacher_report_card_table(teacher_report_list))
        print("")
        report_id = input("Please enter the id of the report card to delete or type 'QUIT' to exit: ")
        report_card = session.query(Report_card).filter_by(id = report_id).first()
        if report_id == "QUIT":
            print("Bye! Thanks for using my app!")
        elif report_card and report_card.teacher_id == teacher.id:
            student = session.query(Student).filter_by(id = report_card.student_id).first()
            confirmation = input(f"Are you sure you want to delete report card ID: {report_card.id} for student: {student.name}? (Type Y/N): ")
            if confirmation in YES:
                session.delete(report_card)
                session.commit()

                print("Report card deleted!")
                time.sleep(2)
                teacher_menu(teacher)
            elif confirmation in NO:
                print("Returning to teacher hub.")
                time.sleep(2)
                teacher_menu(teacher)
            else:
                print("Invalid input - Please retry.")
                time.sleep(2)
                teacher_report_cards_delete(teacher)
        else:
            print("Invalid input - Please retry.")
            time.sleep(2)
            teacher_report_cards_delete(teacher)
    else:
        print("You have not yet created any report cards.")
        time.sleep(2)
        main_menu()

def teacher_new_report_card(teacher):
    print('''
    Please fill out the questions below regarding the new report card.
    ------------------------------------------------------------------
    ''')
    student_name = input(str("Enter students name: "))
    student = session.query(Student).filter_by(name = student_name.title()).first()
    if student:
        n_course = input(str("Enter the course: "))
        n_grade = input(str(f"Enter {student_name.title()}'s grade in {n_course}: "))
        n_feedback = input(str(f"Enter feedback for {student_name}: "))
        new_report_card = Report_card(student_id=student.id, teacher_id=teacher.id, course=n_course, feedback=n_feedback, grade=n_grade.title())

        session.add(new_report_card)
        session.commit()

        print("Report card submitted!")
        time.sleep(2)
        teacher_menu(teacher)
    else:
        print("Error finding student - Please retry")
        time.sleep(2)
        teacher_new_report_card(teacher)

def student_report_card_table(report_cards):
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

def teacher_report_card_table(report_cards):
    table = PrettyTable()
    table.title = " REPORT CARDS "
    table.field_names = ["Report Card ID", "Teacher Name", "Student Name", "Course", "Grade", "Feedback"]
    for report_card in report_cards:
        teacher = session.query(Teacher).filter_by(id = report_card.teacher_id).first()
        student = session.query(Student).filter_by(id = report_card.student_id).first()
        table.add_row([
            report_card.id,
            teacher.name,
            student.name,
            report_card.course,
            report_card.grade,
            report_card.feedback
            ])
    return table
