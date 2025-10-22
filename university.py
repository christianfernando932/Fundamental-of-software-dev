"""
university.py
University System + Authentication routing (lowercase menu)

- University menu: (a) admin / (s) student / (x) exit
- Admin routes to AdminSystem (no admin login per brief)
- Student routes to StudentSystem (login/register/exit) — provided by Person 2
- If StudentSystem not found, fallback student menu allows register/login
  and saves to students.data (visible in Admin → show)
"""

from __future__ import annotations
from typing import List, Dict, Any

from database import Database
from admin import AdminSystem
from validation import is_valid_email, is_valid_password, generate_student_id

# Try importing Person 2's file if it exists
try:
    from student_system import StudentSystem
except ImportError:
    StudentSystem = None  # fallback mode active


# ---------- small utility ----------
def _is_exit(token: str) -> bool:
    token = (token or "").strip().lower()
    return token in {"x", "q", "quit", "exit"}


class UniversityApp:
    def __init__(self, db: Database):
        self.db = db
        self.admin_sys = AdminSystem(db)
        self.student_sys = StudentSystem(db) if StudentSystem else None

    # ----------------- University Menu -----------------
    def start(self) -> None:
        while True:
            print("\nuniversity system")
            print("(a) admin")
            print("(s) student")
            print("(x) exit")
            choice = (input("> ") or "").strip().lower()

            if choice == "a":
                self.admin_sys.menu()

            elif choice == "s":
                if self.student_sys is not None:
                    self.student_sys.menu()           # use real student system (Person 2)
                else:
                    self._student_menu_fallback()     # fallback for now

            elif _is_exit(choice):
                print("goodbye!")
                break

            else:
                print("invalid option. please try again.")

    # ----------------- Fallback Student Menu -----------------
    def _student_menu_fallback(self) -> None:
        while True:
            print("\nthe student system")
            print("(l) login")
            print("(r) register")
            print("(x) exit")
            choice = (input("> ") or "").strip().lower()

            if choice == "l":
                self._login_flow_fallback()
            elif choice == "r":
                self._register_flow_fallback()
            elif _is_exit(choice):
                return
            else:
                print("invalid option. please try again.")

    # ----------------- Login (Fallback) -----------------
    def _login_flow_fallback(self) -> None:
        email = input("enter email (or 'x' to cancel): ").strip()
        if _is_exit(email):
            print("login cancelled.")
            return

        password = input("enter password (or 'x' to cancel): ").strip()
        if _is_exit(password):
            print("login cancelled.")
            return

        if not is_valid_email(email):
            print("error: incorrect email format. (must end with @university.com)")
            return
        if not is_valid_password(password):
            print("error: incorrect password format.")
            print("password must start with an uppercase, contain at least five letters total, and end with three or more digits.")
            return

        student = self.db.find_by_email(email)
        if student and student.get("password") == password:
            print("login successful.")
            # Person 3's Subject Enrolment System can be launched here later
        else:
            print("login failed. please check your credentials.")

    # ----------------- Register (Fallback) -----------------
    def _register_flow_fallback(self) -> None:
        name = input("enter name (or 'x' to cancel): ").strip()
        if _is_exit(name):
            print("registration cancelled.")
            return

        email = input("enter email (or 'x' to cancel): ").strip()
        if _is_exit(email):
            print("registration cancelled.")
            return

        password = input("enter password (or 'x' to cancel): ").strip()
        if _is_exit(password):
            print("registration cancelled.")
            return

        if not name:
            print("error: name cannot be empty.")
            return
        if not is_valid_email(email):
            print("error: incorrect email format. (must end with @university.com)")
            return
        if not is_valid_password(password):
            print("error: incorrect password format.")
            print("password must start with an uppercase, contain at least five letters total, and end with three or more digits.")
            return
        if self.db.find_by_email(email):
            print("registration failed. the student may already exist.")
            return

        existing_ids = [s["id"] for s in self.db.get_all()]
        sid = generate_student_id(existing_ids)
        student = {
            "id": sid,
            "name": name,
            "email": email,
            "password": password,
            "subjects": [],
            # optional convenience fields for Admin seed compatibility:
            "average": 0.0,
            "grade": "Z",
        }

        if self.db.add_student(student):
            print(f"registration successful. your student id is {sid}.")
            print("you can now login or view your record in admin → show.")
        else:
            print("registration failed. the student may already exist.")


# ----------------- Run Standalone -----------------
if __name__ == "__main__":
    app = UniversityApp(Database("students.data"))
    app.start()
