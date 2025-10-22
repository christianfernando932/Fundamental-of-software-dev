# validation.py
"""
Validation utilities for CLIUniApp
- Email/password regex (spec-compliant)
- Unique ID generators (student 6-digit, subject 3-digit with zero-padding)
- Menu input validation
- Simple notify helper

Spec rules:
- Email must end with @university.com
- Password: starts with uppercase, at least 5 letters total, then 3+ digits
"""

from __future__ import annotations
import re
import random
from typing import Iterable, Set

# --------- Regex from the brief ---------
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[Uu][Nn][Ii][Vv][Ee][Rr][Ss][Ii][Tt][Yy]\.com$")
PASSWORD_PATTERN = re.compile(r"^[A-Z][A-Za-z]{4,}\d{3,}$")

def is_valid_email(email: str) -> bool:
    # fullmatch → the whole string must satisfy the pattern
    return EMAIL_PATTERN.fullmatch(email or "") is not None

def is_valid_password(pw: str) -> bool:
    return PASSWORD_PATTERN.fullmatch(pw or "") is not None


# --------- ID generation (zero-padded) ---------
def generate_student_id(existing_ids: Iterable[str] | None = None) -> str:
    """
    Random 1..999999 → zero-padded 6-digit string. Avoid collisions using existing_ids.
    """
    existing: Set[str] = set(existing_ids or [])
    while True:
        sid = f"{random.randint(1, 999_999):06d}"
        if sid not in existing:
            return sid

def generate_subject_id(existing_ids: Iterable[str] | None = None) -> str:
    """
    Random 1..999 → zero-padded 3-digit string. Avoid collisions using existing_ids.
    """
    existing: Set[str] = set(existing_ids or [])
    while True:
        sub_id = f"{random.randint(1, 999):03d}"
        if sub_id not in existing:
            return sub_id


# --------- Menu + notify helpers ---------
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
