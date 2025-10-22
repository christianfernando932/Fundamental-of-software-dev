"""
admin.py
Admin System: show / group students / partition students / remove student / clear database

- Uses the shared Database (students.data). No pickle here.
- Computes Avg/Grade from subjects; falls back to 'average' if present (for seeded demo data).
- Optional seed: ENABLE_SAMPLE_DATA to auto-load demo students if file is empty.
"""

from __future__ import annotations
from typing import Dict, Any, List
from database import Database

# Toggle demo seeding (set to False before final hand-in if you prefer)
ENABLE_SAMPLE_DATA = True

# ---------- helpers for averages/grades ----------
def compute_average(student: Dict[str, Any]) -> float:
    """
    Average mark across enrolled subjects.
    Falls back to a precomputed 'average' field if subjects are missing.
    """
    subjects: List[Dict[str, Any]] = student.get("subjects", []) or []
    if subjects:
        total = sum(int(sub.get("mark", 0)) for sub in subjects)
        return total / len(subjects) if subjects else 0.0
    return float(student.get("average", 0.0))

def mark_to_grade(mark: int) -> str:
    if mark >= 85: return "HD"
    if mark >= 75: return "D"
    if mark >= 65: return "C"
    if mark >= 50: return "P"
    return "Z"

def overall_grade_from_average(avg: float) -> str:
    return mark_to_grade(int(round(avg)))

# ---------- optional seeding ----------
def _seed_if_empty(db: Database) -> None:
    if not ENABLE_SAMPLE_DATA:
        return
    students = db.load_students()
    if students:
        return
    sample_students = [
        {"id": "100001", "name": "Sabna Giri",   "email": "sabna.giri@university.com",
         "subjects": [], "average": 85.5, "grade": "HD"},
        {"id": "100002", "name": "Prerak Patel", "email": "prerak.patel@university.com",
         "subjects": [], "average": 74.0, "grade": "D"},
        {"id": "100003", "name": "Nikita Sharma","email": "nikita.sharma@university.com",
         "subjects": [], "average": 68.2, "grade": "C"},
        {"id": "100004", "name": "Rohit Singh",  "email": "rohit.singh@university.com",
         "subjects": [], "average": 52.5, "grade": "P"},
        {"id": "100005", "name": "Neha Karki",   "email": "neha.karki@university.com",
         "subjects": [], "average": 43.1, "grade": "Z"},
    ]
    db.save_students(sample_students)
    print("✅ Sample data loaded for demo purposes.\n")

# ---------- Admin system ----------
class AdminSystem:
    def __init__(self, db: Database):
        self.db = db

    def menu(self) -> None:
        # Seed once if file is empty
        _seed_if_empty(self.db)

        while True:
            print("\n=== Admin System Menu ===")
            print("(s) show")
            print("(g) group students")
            print("(p) partition students")
            print("(r) remove student")
            print("(c) clear database")
            print("(x) exit")
            choice = input("Select an option: ").strip().lower()

            if choice == "s":
                self.show_all()
            elif choice == "g":
                self.group_students()
            elif choice == "p":
                self.partition_students()
            elif choice == "r":
                self.remove_student()
            elif choice == "c":
                self.clear_database()
            elif choice == "x":
                print("Exiting Admin System...")
                break
            else:
                print("Invalid choice. Please try again.")

    def show_all(self) -> None:
        students = self.db.load_students()
        if not students:
            print("No student records found.")
            return

        print("\n=== All Students ===")
        for s in students:
            avg = compute_average(s)
            overall = overall_grade_from_average(avg)
            print(
                f"ID: {s.get('id')} | Name: {s.get('name')} | Email: {s.get('email')} | "
                f"Avg Mark: {avg:.2f} | Grade: {overall}"
            )

    def group_students(self) -> None:
        students = self.db.load_students()
        if not students:
            print("No student data to group.")
            return

        groups: Dict[str, List[Dict[str, Any]]] = {"HD": [], "D": [], "C": [], "P": [], "Z": []}
        for s in students:
            avg = compute_average(s)
            g = overall_grade_from_average(avg)
            groups[g].append(s)

        print("\n=== Grouped by Grade ===")
        for grade, group_list in groups.items():
            labels = [f"{stu.get('name')} ({stu.get('id')})" for stu in group_list]
            print(f"{grade}: {labels}")

    def partition_students(self) -> None:
        students = self.db.load_students()
        if not students:
            print("No student data to partition.")
            return

        passed, failed = [], []
        for s in students:
            avg = compute_average(s)
            (passed if avg >= 50.0 else failed).append((s, avg))

        print("\n=== Pass Students ===")
        for s, avg in passed:
            print(f"{s.get('name')} ({s.get('id')}) | Avg: {avg:.2f}")

        print("\n=== Fail Students ===")
        for s, avg in failed:
            print(f"{s.get('name')} ({s.get('id')}) | Avg: {avg:.2f}")

    def remove_student(self) -> None:
        students = self.db.load_students()
        if not students:
            print("No student records found.")
            return

        sid = input("Enter student ID to remove: ").strip()
        if not sid:
            print("Invalid ID.")
            return

        removed = self.db.remove_by_id(sid)
        if removed:
            print(f"Student {sid} removed successfully.")
        else:
            print(f"Student with ID {sid} not found.")

    def clear_database(self) -> None:
        confirm = input("Are you sure you want to clear all student data? (y/n): ").strip().lower()
        if confirm == "y":
            self.db.clear()
            print("All student data cleared.")
        else:
            print("Operation cancelled.")

# Standalone test
if __name__ == "__main__":
    db = Database("students.data")
    AdminSystem(db).menu()
