from database import Database                      # your team's storage layer
from validation import (
    is_valid_email, is_valid_password,             # regex checks
    generate_student_id,                           # id + menu helper
    notify                                         # standardised messages
)

def student_menu(db: Database):
    while True:
        print("\n--- Student Menu ---")
        print("(l) login")
        print("(r) register")
        print("(x) exit")
        choice = input("Enter choice: ").strip().lower()

        if choice == "l":
            stu = login_student(db)
            if stu:
                notify(f"Welcome back, {stu['name']}!")
                return stu  # hand over to enrolment menu in main flow
        elif choice == "r":
            register_student(db)
        elif choice == "x":
            notify("Returning to main menu.")
            return None
        else:
            notify("Invalid choice. Use l, r, or x.")

def register_student(db: Database):
    print("\n--- Register ---")
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()

    # 1) regex checks from validation.py
    if not is_valid_email(email):
        notify("Invalid email. Must end with @university.com")
        return
    if not is_valid_password(password):
        notify("Invalid password. Start with uppercase, 5+ letters, then 3+ digits.")
        return

    # 2) load all students and block duplicate email
    if db.find_by_email(email):
        notify("A student with that email already exists.")
        return

    students = db.load_students()
    new_id = generate_student_id([s["id"] for s in students])

    # 3) unique 6-digit ID using helper (avoid collisions)
    existing_ids = [s.get("id") for s in students]

    # 4) create record (dict matches database schema)
    new_student = {
        "id": new_id,
        "name": name,
        "email": email,
        "password": password,
        "subjects": [],
        "average": 0.0,
        "grade": "Z"
    }

    # 5) save (append) to students.data via database.py
    if db.add_student(new_student):
        notify(f"Registration successful! Your ID is {new_id}")
    else:
        notify("Registration failed (duplicate or write error).")
    
def login_student(db: Database):
    print("\n--- Login ---")
    email = input("Email: ").strip()
    password = input("Password: ").strip()

    if not is_valid_email(email) or not is_valid_password(password):
        notify("Invalid credentials format.")
        return None

    s = db.find_by_email(email)
    if s and s.get("password") == password:
        return s

    notify("Invalid credentials.")
    return None
