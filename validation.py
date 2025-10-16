# validation.py
"""
Validation utilities for CLIUniApp
- Email/password regex (spec-compliant)
- Unique ID generators (student 6-digit, subject 3-digit with zero-padding)
- Menu input validation
- Simple notify helper
"""

from __future__ import annotations
import re
import random
from typing import Iterable, Set

# --------- Regex from the brief ---------
# Email must end with @university.com (firstname.lastname@university.com is valid)
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[Uu][Nn][Ii][Vv][Ee][Rr][Ss][Ii][Tt][Yy]\.com$")

# Password rules:
# 1) Starts with uppercase letter
# 2) Contains at least five letters total
# 3) Followed by three or more digits
#
# One simple, strict interpretation:
#   ^[A-Z][A-Za-z]{4,}\d{3,}$
PASSWORD_PATTERN = re.compile(r"^[A-Z][A-Za-z]{4,}\d{3,}$")


def is_valid_email(email: str) -> bool:
    return EMAIL_PATTERN.match(email or "") is not None


def is_valid_password(pw: str) -> bool:
    return PASSWORD_PATTERN.match(pw or "") is not None


# --------- ID generation (zero-padded) ---------
def generate_student_id(existing_ids: Iterable[str] | None = None) -> str:
    """
    Random 1..999999 → zero-padded 6-digit string. Avoid collisions using existing_ids.
    """
    existing: Set[str] = set(existing_ids or [])
    # In practice there will be very few, so a simple loop is fine.
    while True:
        n = random.randint(1, 999_999)
        sid = f"{n:06d}"
        if sid not in existing:
            return sid


def generate_subject_id(existing_ids: Iterable[str] | None = None) -> str:
    """
    Random 1..999 → zero-padded 3-digit string. Avoid collisions using existing_ids.
    """
    existing: Set[str] = set(existing_ids or [])
    while True:
        n = random.randint(1, 999)
        sub_id = f"{n:03d}"
        if sub_id not in existing:
            return sub_id


# --------- Menu helpers ---------
def validate_menu_choice(choice: str, allowed: set[str]) -> bool:
    """
    Return True iff user choice is in allowed set, case-insensitive.
    """
    if not choice:
        return False
    return choice.strip().lower() in {a.lower() for a in allowed}


def notify(msg: str) -> None:
    """
    Simple place to standardise system messages (extend later if needed).
    """
    print(f"[SYSTEM] {msg}")
