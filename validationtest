# test_validation_solo.py
from validation import is_valid_email, is_valid_password, generate_student_id, generate_subject_id

def run():
    print("== EMAIL TESTS ==")
    emails = [
        "alice@university.com",      # ✅ valid
        "Bob.Smith@UNIVERSITY.com",  # ✅ valid (case-insensitive domain)
        "charlie@gmail.com",         # ❌ invalid
        "no-at-sign",                # ❌ invalid
        "d@university"               # ❌ invalid
    ]
    for e in emails:
        print(f"{e:30} -> {is_valid_email(e)}")

    print("\n== PASSWORD TESTS ==")
    pwds = [
        "StartX999",      # ✅ valid (Upper + >=5 letters + >=3 digits)
        "Abcde12345",     # ✅ valid
        "abcde12345",     # ❌ invalid (must start uppercase)
        "Aabc1",          # ❌ invalid (needs >=5 letters then >=3 digits)
        "Aabcd12",        # ❌ invalid (only 2 digits)
        "Zzzzz000",       # ✅ valid
    ]
    for p in pwds:
        print(f"{p:12} -> {is_valid_password(p)}")

    print("\n== ID GENERATION ==")
    existing_students = {"000001", "123456"}
    sid = generate_student_id(existing_students)
    print(f"New student ID (not in {existing_students}): {sid}")

    existing_subjects = {"001", "250", "999"}
    subid = generate_subject_id(existing_subjects)
    print(f"New subject ID (not in {existing_subjects}): {subid}")

if __name__ == "__main__":
    run()

