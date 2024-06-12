# lib/cli.py
import click
from models.school import School
from models.course import Course
from models.student import Student

@click.group()
def cli():
    pass

@click.command()
def create_tables():
    School.create_table()
    Course.create_table()
    Student.create_table()
    click.echo("Tables created.")

@click.command()
def drop_tables():
    School.drop_table()
    Course.drop_table()
    Student.drop_table()
    click.echo("Tables dropped.")

@click.command()
@click.option('--name', prompt='School name', help='The name of the school.')
@click.option('--location', prompt='School location', help='The location of the school.')
def add_school(name, location):
    school = School.create(name, location)
    click.echo(f"School added: {school}")

@click.command()
def list_schools():
    schools = School.get_all()
    for school in schools:
        click.echo(school)

@click.command()
@click.option('--name', prompt='School name', help='The name of the school.')
def find_school(name):
    school = School.find_by_name(name)
    if school:
        click.echo(f"Found school: {school}")
    else:
        click.echo("School not found.")

@click.command()
@click.option('--title', prompt='Course title', help='The title of the course.')
@click.option('--description', prompt='Course description', help='The description of the course.')
@click.option('--school_id', prompt='School ID', type=int, help='The ID of the school offering the course.')
def add_course(title, description, school_id):
    course = Course.create(title, description, school_id)
    click.echo(f"Course added: {course}")

@click.command()
def list_courses():
    courses = Course.get_all()
    for course in courses:
        click.echo(course)

@click.command()
@click.option('--name', prompt='Student name', help='The name of the student.')
@click.option('--student_id', prompt='Student ID', type=int, help='The ID of the student.')
def add_student(name, student_id):
    student = Student.create(name, student_id)
    click.echo(f"Student added: {student}")

@click.command()
def list_students():
    students = Student.get_all()
    for student in students:
        click.echo(student)

cli.add_command(create_tables)
cli.add_command(drop_tables)
cli.add_command(add_school)
cli.add_command(list_schools)
cli.add_command(find_school)
cli.add_command(add_course)
cli.add_command(list_courses)
cli.add_command(add_student)
cli.add_command(list_students)

if __name__ == '__main__':
    cli()
