# test_database_solo.py
import os
from database import Database

TMP_FILE = "tmp_students.data"

def show(db, heading):
    print(f"\n== {heading} ==")
    for s in db.load_students():
        print(f"{s['id']} | {s['name']} | {s['email']} | subjects={len(s.get('subjects', []))}")

def run():
    # start fresh
    if os.path.exists(TMP_FILE):
        os.remove(TMP_FILE)

    db = Database(TMP_FILE)

    # 1) empty file should be auto-created
    print("File exists after init:", os.path.exists(TMP_FILE))
    print("Initially:", db.load_students())  # should be []

    # 2) add 2 students
    s1 = {"id": "700001", "name": "Alice", "email": "alice@university.com", "password": "StartX999", "subjects": []}
    s2 = {"id": "700002", "name": "Bob",   "email": "bob@university.com",   "password": "StartX999", "subjects": []}
    ok1 = db.add_student(s1)
    ok2 = db.add_student(s2)
    print("Add Alice:", ok1, "Add Bob:", ok2)

    # 3) duplicate email should fail
    dup = {"id": "700003", "name": "Alice2", "email": "alice@university.com", "password": "StartX999", "subjects": []}
    print("Add duplicate email:", db.add_student(dup))  # False

    show(db, "AFTER INSERT")

    # 4) find by id/email
    print("find_by_id 700001:", db.find_by_id("700001"))
    print("find_by_email bob@university.com:", db.find_by_email("bob@university.com"))

    # 5) update Bob (add a subject)
    bob = db.find_by_id("700002")
    bob["subjects"].append({"id": "101", "mark": 80, "grade": "D"})
    db.update_student(bob)
    show(db, "AFTER UPDATE (Bob 1 subject)")

    # 6) remove Alice
    removed = db.remove_by_id("700001")
    print("Removed Alice:", removed)
    show(db, "AFTER REMOVE")

    # 7) clear all
    db.clear()
    show(db, "AFTER CLEAR (should be empty)")

    # cleanup temp file (optional)
    try:
        os.remove(TMP_FILE)
        print("\nTemp file removed.")
    except OSError:
        pass

if __name__ == "__main__":
    run()
