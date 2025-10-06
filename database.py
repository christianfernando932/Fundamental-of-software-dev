# database.py
"""
Database layer for CLIUniApp.
- File: students.data (JSON array)
- Operations: init/check file, read all, write all, append, find/remove by ID, clear
Safe JSON handling with graceful fallbacks.
"""

from __future__ import annotations
import json
import os
import tempfile
from typing import List, Dict, Optional

DATA_FILE = "students.data"


class DatabaseError(Exception):
    """Generic database exception."""


class Database:
    def __init__(self, file_path: str = DATA_FILE):
        self.file_path = file_path
        self.initialise_storage()

    # ---------- File existence / initialization ----------

    def initialise_storage(self) -> None:
        """
        Ensure students.data exists and is a valid JSON array.
        If file is empty or corrupt, re-write as [].
        """
        if not os.path.exists(self.file_path):
            self._write_json_atomic([])
            return

        # If exists, make sure it contains a JSON array
        try:
            data = self._read_json()
            if not isinstance(data, list):
                # reset to empty list
                self._write_json_atomic([])
        except json.JSONDecodeError:
            # Corrupt or empty → reset gracefully
            self._write_json_atomic([])

    # ---------- Low-level JSON I/O ----------

    def _read_json(self) -> List[Dict]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            txt = f.read().strip()
            if not txt:
                return []
            return json.loads(txt)

    def _write_json_atomic(self, data: List[Dict]) -> None:
        """
        Atomic write to avoid corruption: write to temp file then replace.
        """
        dir_name = os.path.dirname(os.path.abspath(self.file_path)) or "."
        fd, tmp_path = tempfile.mkstemp(dir=dir_name, prefix="._students_", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as tmp:
                json.dump(data, tmp, indent=2)
            os.replace(tmp_path, self.file_path)
        except Exception as e:
            # Clean up temp file on failure
            try:
                os.remove(tmp_path)
            except Exception:
                pass
            raise DatabaseError(f"Failed to write database: {e}") from e

    # ---------- High-level operations ----------

    def load_all_students(self) -> List[Dict]:
        """
        Returns a list of student dicts.
        Schema (expected by controllers):
        {
          "id": "000123",
          "name": "Alice",
          "email": "alice@university.com",
          "password": "HashedOrPlainPerYourDesign",
          "subjects": [
              {"id": "001", "mark": 72, "grade": "C"},
              ...
          ]
        }
        """
        return self._read_json()

    def write_all_students(self, students: List[Dict]) -> None:
        """
        Overwrite the entire file with the provided list.
        """
        self._write_json_atomic(students)

    def append_student(self, student: Dict) -> None:
        """
        Add a new student to the file.
        """
        students = self.load_all_students()
        students.append(student)
        self._write_json_atomic(students)

    def find_student_by_id(self, student_id: str) -> Optional[Dict]:
        """
        Find a single student by 6-digit string id (e.g., '000123').
        """
        students = self.load_all_students()
        for s in students:
            if s.get("id") == student_id:
                return s
        return None

    def remove_student_by_id(self, student_id: str) -> bool:
        """
        Remove a student by id. Returns True if deleted, False if not found.
        """
        students = self.load_all_students()
        new_list = [s for s in students if s.get("id") != student_id]
        removed = len(new_list) != len(students)
        if removed:
            self._write_json_atomic(new_list)
        return removed

    def clear_all(self) -> None:
        """
        Remove all students.
        """
        self._write_json_atomic([])

    # ---------- Subject helpers (optional, handy for Person 3) ----------

    def update_student(self, updated: Dict) -> None:
        """
        Replace a student record with matching id.
        """
        sid = updated.get("id")
        if not sid:
            raise DatabaseError("Student has no id.")
        students = self.load_all_students()
        for i, s in enumerate(students):
            if s.get("id") == sid:
                students[i] = updated
                self._write_json_atomic(students)
                return
        raise DatabaseError(f"Student id {sid} not found.")
