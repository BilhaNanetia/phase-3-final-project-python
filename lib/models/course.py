# lib/models/course.py
from models.__init__ import CURSOR, CONN
from models.school import School

class Course:
    all = {}

    def __init__(self, title, description, school_id, id=None):
        self.id = id
        self.title = title
        self.description = description
        self.school_id = school_id

    def __repr__(self):
        return f"<Course {self.id}: {self.title}, {self.description}, School ID: {self.school_id}>"

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str) and len(title):
            self._title = title
        else:
            raise ValueError("Title must be a non-empty string")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if isinstance(description, str) and len(description):
            self._description = description
        else:
            raise ValueError("Description must be a non-empty string")

    @property
    def school_id(self):
        return self._school_id

    @school_id.setter
    def school_id(self, school_id):
        if isinstance(school_id, int) and School.find_by_id(school_id):
            self._school_id = school_id
        else:
            raise ValueError("school_id must reference a school in the database")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            school_id INTEGER,
            FOREIGN KEY (school_id) REFERENCES schools(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS courses"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = "INSERT INTO courses (title, description, school_id) VALUES (?, ?, ?)"
        CURSOR.execute(sql, (self.title, self.description, self.school_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, title, description, school_id):
        course = cls(title, description, school_id)
        course.save()
        return course

    def update(self):
        sql = "UPDATE courses SET title = ?, description = ?, school_id = ? WHERE id = ?"
        CURSOR.execute(sql, (self.title, self.description, self.school_id, self.id))
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM courses WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        course = cls.all.get(row[0])
        if course:
            course.title = row[1]
            course.description = row[2]
            course.school_id = row[3]
        else:
            course = cls(row[1], row[2], row[3])
            course.id = row[0]
            cls.all[course.id] = course
        return course

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM courses"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM courses WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_title(cls, title):
        sql = "SELECT * FROM courses WHERE title = ?"
        row = CURSOR.execute(sql, (title,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def students(self):
        from models.student import Student
        sql = "SELECT * FROM students WHERE course_id = ?"
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Student.instance_from_db(row) for row in rows]
