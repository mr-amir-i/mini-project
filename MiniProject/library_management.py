import json
import os
from datetime import date

MENU = """
========================================
       LIBRARY MANAGEMENT SYSTEM
========================================
          
    1. Add New Book
    2. Display All Books
    3. Search Books
    4. Edit Book Information
    5. Delete Book
    6. Borrow Book
    7. Return Book
    8. View Borrowed Books
    9. Show Library Statistics
    0. Exit
          
"""

board = '┌'+'─'*106+'┐'
details = f"│{'ID':<3}│{'Title':<41}│{'Author':<25}│{'Year':<4}│{'Genre':<20}│{'TC':<2}│{'AC':<2}│{'BC':<2}│"
board2 = '└'+'─'*106+'┘'

ADD_FIELDS =["ID","Title","Author","Year","Genre","Total_Copies","Available_Copies","Borrowed_Copies"]

def print_all(book):
    print(f"│{book['ID']:<3}│{book['Title']:<41}│{book['Author']:<25}│{book['Year']:<4}│{book['Genre']:<20}│{book['Total_Copies']:<2}│{book['Available_Copies']:<2}│{book['Borrowed_Copies']:<2}│")

def show_table(book):
    if not book:
        print("No books found")
        return
    print(board)
    print(details)
    for bok in book:
        print_all(bok)
    print(board2)

def check(field, value, data):
    if value == "":
        return "This field cannot be empty"

    if field == "ID":
        if not value.isdigit():
            return "ID must be a number"

        for bok in data:
            if value == str(bok["ID"]):
                return "Book ID already exists"

    elif field in ("Title", "Author","Genre"):
        if len(value) < 2:
            return f"{field} is too short"

    elif field == "Year":
        if not value.isdigit():
            return "Year must be a number"

        if not 1000 <= int(value) <= date.today().year:
            return f"Year must be between 1000 and {date.today().year}"

    elif field in ("Total_Copies","Available_Copies", "Borrowed_Copies"):
        if not value.isdigit():
            return f"{field} must be a non-negative number"

    return ""

def read_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding= "utf-8") as read_file:
        return json.load(read_file)

def write_data(filename, data):
    with open(filename, "w",encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def add_book():
    data = read_data("books.json")
    book = {}
    for field in ADD_FIELDS:
        while True:
            value = input(f"Please enter book {field}: ").strip()
            error = check(field, value, data)
            if error == "":
                break
            print(error)
        book[field] = value
    for field in ADD_FIELDS:
        if field in ("ID", "Year", "Total_Copies", "Available_Copies", "Borrowed_Copies"):
            book[field] = int (book[field])

    data.append(book)
    write_data("books.json",data)
    print("Book added!")

def display_books():
    show_table(read_data("books.json"))
    input("Press Enter to continue...")

def search_books():
    data = read_data("books.json")
    search = input("Search Books: ").strip().lower()
    book = []
    for bok in data:
        if search in (str(bok["ID"]), bok["Title"].lower(), bok["Author"].lower(), bok["Genre"].lower()):
            book.append(bok)
    show_table(book)
    input("Press Enter to continue...")

def edit_book():
    data = read_data("books.json")
    search = input("Search Books: ").strip().lower()
    book_edit = ["Total_Copies", "Available_Copies", "Borrowed_Copies"]

    for bok in data:

        if search in (str(bok["ID"]), bok["Title"].lower()):
            show_table([bok])
            print(book_edit)
            field = input("What would you like to edit: ")

            if field in book_edit:
                new = input(f"What would you like to edit {field}: ")
                error = check(field, new, data)
                if error == "":
                    bok[field] = int(new)
                    write_data("books.json",data)
                    print("Book edited!")

                else:
                    print(error)

            else:
                print("Invalid input!")

            return
    print("book not found!")

def delete_book():
    data = read_data("books.json")
    search = input("Search Books: ").strip().lower()

    for bok in data:

        if search in (str(bok["ID"]), bok["Title"].lower()):
            show_table([bok])
            sure = input("Would you like to delete this book? (y/n): ")

            if sure == "y":
                data.remove(bok)
                write_data("books.json",data)
                print("Book deleted!")
            else:
                print("Deletion cancelled!")
            return

    print("book not found!")


FIELDS_BORROW = ["Borrow_ID", "Book_ID", "Borrower_Name", "Borrow_Date", "Returned_Date", "Status"]

def print_borrowed_books(data):
    print(f"| {'BwID':<4}| {'BkID':<4}| {'Borrower_Name':<15}| {'Borrow_Date':<15}| {'Returned_Date':<13}| {'Status':8}|")
    for bor in data:
        print(f"| {bor['Borrow_ID']:<4}| {bor['Book_ID']:<4}| {bor['Borrower_Name']:<15}| {bor['Borrow_Date']:<15}| {bor['Returned_Date']:<13}| {bor['Status']}|")

def borrow_book():
    data = read_data("borrowed_books.json")
    
    borrow = {}
    for field in FIELDS_BORROW:

        if field == "Borrow_Date":
            borrow[field] = str(date.today())
            continue

        value = input(f"Please enter book {field}: ").strip()
        borrow[field] = value

    for field in FIELDS_BORROW:

        if field in ("Borrow_ID", "Book_ID"):
            borrow[field] = int(borrow[field])
    data.append(borrow)
    print_borrowed_books([borrow])
    write_data("borrowed_books.json", data)
    print("add borrowed book!")

def return_book():
    data = read_data("borrowed_books.json")
    borrow = int(input("Please, enter Borrow_ID: "))
    for bor in data:

        if borrow == bor["Borrow_ID"]:

            if bor["Returned_Date"] is None:
                bor['Returned_Date'] = '----'

            print_borrowed_books([bor])
            new = input("Do you want to return this book? (y/n): ")

            if new == "y":
                bor["Returned_Date"] = str(date.today())
                bor["Status"] = "Returned"
                print("Book returned!")
            else:
                print("Book not returned!")
    write_data("borrowed_books.json",data)


def display_borrowed_books():
    data = read_data("borrowed_books.json")
    borrow = input("Borrowed or Returned: ").strip().capitalize()
    borrowed = []
    for bor in data:

        if bor["Status"]==borrow:

            if bor["Returned_Date"] is None:
                bor['Returned_Date'] = '----'
            borrowed.append(bor)
    print_borrowed_books(borrowed)

def show_statistics():
    data = read_data("borrowed_books.json")
    data_book = read_data("books.json")

    total_book = 0
    total_copies = 0
    available_copies = 0
    borrowed_copies = 0

    total_borrow = 0
    active_borrow = 0
    returned_book = 0
    for bok in data_book:
        total_book += 1
        total_copies += bok["Total_Copies"]
        available_copies += bok["Available_Copies"]
        borrowed_copies += bok["Borrowed_Copies"]
    for bor in data:
        total_borrow += 1
        if bor["Status"]=="Borrowed":
            active_borrow += 1
        if bor["Status"]=="Returned":
            returned_book += 1
    print(f"Total books: {total_book}\n"
          f"Total copies: {total_copies}\n"
          f"Available borrows: {available_copies}\n"
          f"Borrowed copies: {borrowed_copies}\n"
          f"\n"
          f"Total borrowed book: {total_borrow}\n"
          f"Available borrowed: {active_borrow}\n"
          f"Returned book: {returned_book}\n")

OPTION = {
    "1": add_book,
    "2": display_books,
    "3": search_books,
    "4": edit_book,
    "5": delete_book,
    "6": borrow_book,
    "7": return_book,
    "8": display_borrowed_books,
    "9": show_statistics,
}


def main():
    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        option = OPTION.get(choice)
        if option:
            option()
        else:
            print("Invalid input! Please enter a number between 0 and 9.")

if __name__ == "__main__":
    main()