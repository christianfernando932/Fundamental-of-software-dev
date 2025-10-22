"""
database.py
Pickle-backed Database for Student records stored in students.data

Student dict structure expected:
{
  "id": "000123",
  "name": "Alice",
  "email": "alice@university.com",
  "password": "StartX999",
  "subjects": [
      {"id": "101", "mark": 78, "grade": "D"},
      ...
  ]
}
"""

from __future__ import annotations
import os
import pickle
from typing import List, Dict, Any, Optional

Student = Dict[str, Any]

class Database:
    def __init__(self, filename: str = "students.data"):
        self.filename = filename
        folder = os.path.dirname(self.filename)
        if folder:
            os.makedirs(folder, exist_ok=True)
        if not os.path.exists(self.filename):
            with open(self.filename, "wb") as f:
                pickle.dump([], f)

    # ---- core file ops ----
    def _read(self) -> List[Student]:
        try:
            with open(self.filename, "rb") as f:
                data = pickle.load(f)
                return data if isinstance(data, list) else []
        except (EOFError, FileNotFoundError, pickle.PickleError):
            return []

    def _write(self, students: List[Student]) -> None:
        with open(self.filename, "wb") as f:
            pickle.dump(students, f)

    # ---- public API used by the app ----
    def load_students(self) -> List[Student]:
        return self._read()

    def save_students(self, students: List[Student]) -> None:
        self._write(students)

    def clear(self) -> None:
        self._write([])

    # ---- convenience helpers for subsystems ----
    def get_all(self) -> List[Student]:
        return self._read()

    def save_all(self, students: List[Student]) -> None:
        self._write(students)

    def find_by_id(self, sid: str) -> Optional[Student]:
        sid = str(sid)
        for s in self._read():
            if str(s.get("id")) == sid:
                return s
        return None

    def find_by_email(self, email: str) -> Optional[Student]:
        for s in self._read():
            if s.get("email") == email:
                return s
        return None

    def add_student(self, student: Student) -> bool:
        rows = self._read()
        if any(r.get("email") == student.get("email") for r in rows):
            return False
        rows.append(student)
        self._write(rows)
        return True

    def update_student(self, student: Student) -> None:
        rows = self._read()
        for i, r in enumerate(rows):
            if r.get("id") == student.get("id"):
                rows[i] = student
                break
        self._write(rows)

    def remove_by_id(self, sid: str) -> bool:
        rows = self._read()
        new_rows = [r for r in rows if str(r.get("id")) != str(sid)]
        removed = len(new_rows) < len(rows)
        if removed:
            self._write(new_rows)
        return removed
