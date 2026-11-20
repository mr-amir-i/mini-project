"""Student Management system. Data is stored in students.csv"""
import csv
import os

MENU = """Select one of the following options to manage students:
    1.Register a New Student   2.Display All Students 
    3.Search for a Student     4.Edit Student information 
    5.Delete a Student         6.Sort Student 
    7.Statistics and Reports   8.Exit the program
"""

# Table borders and header for printing students
board = f"{'┌'}{'─'*93}{'┐'}"
details = f"│{'ID':<3}│{'Gender':<7}│{'Name':<10}│{'Last_Name':<10}│{'Age':<3}│{'National_code':<13}│{'Grade':<3}│{'Field':<12}│{'Average':<7}│{'Phone_number':<14}│"
board2 = f"{'└'}{'─'*93}{'┘'}"

# CSV column names, in file order
FIELDS = ["ID", "Gender", "Name", "Last_Name", "Age", "National_code", "Grade", "Field", "Average", "Phone_number"]

def print_row(std):
    """Print one student as a table row"""
    print(f"│{std["ID"]:<3}│{std["Gender"]:<7}│{std["Name"]:<10}│{std["Last_Name"]:<10}│{std["Age"]:<3}│{std["National_code"]:<13}│{std["Grade"]:5}│{std["Field"]:<12}│{std["Average"]:<7}│{std["Phone_number"]:<14}│")

def show_table(students_data):
    """Print students as a table."""
    if not students_data:
        print("No students found")
        return
    print(board)
    print(details)
    for std in students_data:
        print_row(std)
    print(board2)

def read_data():
    """Load all students from the CSv file"""
    if not os.path.exists('students.csv'):
        return []
    with open("students.csv", newline="", encoding="utf-8") as file:
        return  list(csv.DictReader(file))

def write_data(students_data, mode):
    """mode 'w' rewrites the file, 'a' append """
    if isinstance(students_data, dict):
        students_data = [students_data]
    need_header = (mode == "w" or not os.path.exists('students.csv')
                   or os.path.getsize('students.csv') == 0)
    with open("students.csv", mode, newline="", encoding="utf-8")as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if need_header:
            writer.writeheader()
        writer.writerows(students_data)

def check(field, value, display):
    """validata a field. Returns an error message, or "" if valid"""
    if value == "":
        return "This field cannot be empty"
    if field == "ID":
        if not value.isdigit():
            return "ID must be a number"
        for std in display:
            if std["ID"] == value:
                return "This ID already exists"
    elif field == "Gender":
        if value.lower() not in ["male", "female"]:
            return "Enter male or female"
    elif field == "Age":
        if not value.isdigit() or not 16<= int(value) <= 18:
            return "Age must be between 16 and 18"
    elif field == "National_code":
        if not value.isdigit() or len(value) != 10:
            return "National code must be 10 digits"
        for std in display:
            if std["National_code"] == value:
                return "This National code already exists"
    elif field == "Average":
        try:
            if not 0<= float(value) <= 20:
                return "Average must be between 0 and 20"
        except ValueError:
            return "Average must be number"
    elif field == "Phone_number":
        if not value.isdigit() or len(value) != 11 or not value.startswith("09"):
            return "Phone number must be 11 digits and start with 09"
    return ""

def register_student():
    """Ask for each field, validata it and save the student"""
    display = read_data()
    student = {}
    for field in FIELDS:
        while True:
            value = input(f"Please enter the student {field}:").strip()
            error = check(field, value, display)
            if error == "":
                break
            print(error)
        student[field] = value
    write_data(student , "a")
    print("Student registered")

def display_student():
    """ Show all students """
    display = read_data()
    show_table(display)
    input("Press any key to back")

def search_student():
    """find student by ID, name or last name"""
    display = read_data()
    search = input("Please enter the student you want to search:").strip().lower()
    result = []
    for std in display:
        if search in (std["ID"].lower(), std["Name"].lower(), std["Last_Name"].lower()):
            result.append(std)
    show_table(result)
    input("Press any key to back")


def edit_student():
    """Change one field of a student"""
    display = read_data()
    search = input("Please enter the student you want to edit:").strip().lower()
    for std in display:
        if search in (std["ID"].lower(), std["Name"].lower(), std["Last_Name"].lower()):
            show_table([std])
            print(FIELDS)
            field = input("What would you like to change:")
            if field in FIELDS and field != "ID":
                new = input(f"Please enter the new value:").strip()
                error = check(field, new, display)
                if error == "":
                    std[field] = new
                    write_data(display, "w")
                    print("Student updated")
                else:
                    print(error)
            else:
                print("invalid input")
            return
    print("Student not found.")


def delete_student():
    """Delete a student after confirmation"""
    display = read_data()
    search = input("Please enter the student you want to delete:").strip().lower()
    for std in display:
        if search in (std["ID"].lower(), std["Name"].lower(), std["Last_Name"].lower()):
            show_table([std])
            sure = input("Are you sure you want to delete?(y/n):").lower()
            if sure == "y":
                display.remove(std)
                write_data(display, "w")
                print("student deleted")
            else:
                print("Deletion cancelled")
            return
    print("Student not found.")

def sort_student():
    """filter student by age, grade, gender, field or average"""
    display = read_data()
    search = input("Please enter the student you want to sort:").strip().lower()
    result = []
    if search.lower() in ("age", "grade", "gender", "field"):
        wanted = input(f"Which {search}:").strip().lower()
        for stud in display:
            if stud[search.capitalize()].lower() == wanted:
                result.append(stud)
    elif search == "average":
        try:
            limit = float(input("Average: "))
            way = input("Higher or Lower?").strip().lower()
        except ValueError:
            print("Average must be number")
        for stud in display:
            avg = float(stud["Average"])
            try:
                if (way == "higher" and avg> limit) or (way == "lower" and avg < limit):
                    result.append(stud)
            except ValueError:
                print("Average must be number")
    else:
        print("invalid input")
        return
    show_table(result)
    input("Press any key to back")

def show_student():
    """Show statistics: count, average, highest, lowest, pass/fail"""
    display = read_data()
    if not display:
        print("Student not found.")
        return
    total = 0
    best = 0
    worst = 20
    passed = []
    failed = []
    for std in display:
        avg = float(std["Average"])
        total += avg
        if avg > best:
            best = avg
        if avg < worst:
            worst = avg
        if avg >= 13:
            passed.append(std)
        else:
            failed.append(std)
    print(f"Total students: {len(display)}\n"
          f"Average of averages: {total/len(display):.2f}\n"
          f"Highest average: {best}\n"
          f"Lowest average: {worst}\n"
          f"Passed (13 and above): {len(passed)}\n"
          f"Failed (below 13): {len(failed)}")
    input("Press any key to back")

ACTION = {
    "1": register_student,
    "2": display_student,
    "3": search_student,
    "4": edit_student,
    "5": delete_student,
    "6": sort_student,
    "7": show_student,
}

def main():
    """Run the menu loop until user exits"""
    while True:
        print(MENU)
        choice = input("Which option would you like to select to perform an operation:")
        if choice == "8":
            print("Thank you for using this program")
            break
        action = ACTION.get(choice)
        if action:
            action()
        else:
            print("invalid option, please try again")

if __name__ == "__main__":
    main()