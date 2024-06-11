#!/usr/bin/env python3

from lib.models.__init__ import CONN, CURSOR
from lib.models.school import School
from lib.models.course import Course
from lib.models.student import Student
import ipdb


def reset_database():
    Student.drop_table()
    Course.drop_table()
    School.drop_table()
    School.create_table()
    Course.create_table()
    Student.create_table()

    # Create seed data
    school1 = School.create("Greenwood High", "123 Maple St")
    school2 = School.create("Lakeside Elementary", "456 Oak St")
    
    course1 = Course.create("Math 101", "Basic Mathematics", school1.id)
    course2 = Course.create("History 101", "World History", school1.id)
    course3 = Course.create("Science 101", "Basic Science", school2.id)
    
    student1 = Student.create("Alice", "S123")
    student2 = Student.create("Bob", "S456")
    student3 = Student.create("Charlie", "S789")
    
    student1.enroll(course1)
    student2.enroll(course2)
    student3.enroll(course3)
    student1.enroll(course3)


reset_database()
ipdb.set_trace()
