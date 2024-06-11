# lib/models/student.py
from models.__init__ import CURSOR, CONN
from models.course import Course

class Student:
    all = {}

    def __init__(self, name, student_id, id=None):
        self.id = id
        self.name = name
        self.student_id = student_id

    def __repr__(self):
        return f"<Student {self.id}: {self.name}, {self.student_id}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def student_id(self):
        return self._student_id

    @student_id.setter
    def student_id(self, student_id):
        if isinstance(student_id, int):
            self._student_id = student_id
        else:
            raise ValueError("Student ID must be an integer")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            student_id INTEGER)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS students"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = "INSERT INTO students (name, student_id) VALUES (?, ?)"
        CURSOR.execute(sql, (self.name, self.student_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, student_id):
        student = cls(name, student_id)
        student.save()
        return student

    def update(self):
        sql = "UPDATE students SET name = ?, student_id = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.student_id, self.id))
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM students WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        student = cls.all.get(row[0])
        if student:
            student.name = row[1]
            student.student_id = row[2]
        else:
            student = cls(row[1], row[2])
            student.id = row[0]
            cls.all[student.id] = student
        return student

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM students"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM students WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM students WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
