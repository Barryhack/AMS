from app import create_app, db
from app.models.user import User
from app.models.department import Department
from app.models.course import Course
from app.models.lecture import Lecture
from app.models.attendance import Attendance
from app.models.login_log import LoginLog
from app.models.activity_log import ActivityLog
from app.models.faculty import Faculty
import os

def setup_database():
    """Set up the database from scratch"""
    app = create_app()
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
        print("Created logs directory")
    
    with app.app_context():
        try:
            # Drop all tables if they exist
            db.drop_all()
            
            # Create all tables
            db.create_all()
            
            # Create default admin user
            admin = User(
                id='AD001',
                name='Administrator',
                email='admin@unilorin.edu.ng',
                role='admin',
                is_active=True
            )
            admin.set_password('Admin123!')
            db.session.add(admin)
            
            # Create faculties
            faculties_data = [
                ('Science', 'SCI'),
                ('Engineering', 'ENG'),
                ('Arts', 'ART')
            ]
            
            faculties = {}
            for name, code in faculties_data:
                faculty = Faculty(name=name, code=code)
                faculties[code] = faculty
                db.session.add(faculty)
            
            # Create departments with codes
            departments_data = [
                ('Computer Science', 'CSC', 'SCI'),
                ('Electrical Engineering', 'EEE', 'ENG'),
                ('Mathematics', 'MTH', 'SCI'),
                ('Physics', 'PHY', 'SCI'),
                ('Chemistry', 'CHM', 'SCI')
            ]
            
            departments = {}
            for name, code, faculty_code in departments_data:
                dept = Department(name=name, code=code, faculty=faculties[faculty_code])
                departments[code] = dept
                db.session.add(dept)
            
            # Create lecturers
            lecturers_data = [
                ('John Doe', 'john.doe@unilorin.edu.ng', 'CSC', 'LC001'),
                ('Jane Smith', 'jane.smith@unilorin.edu.ng', 'EEE', 'LC002'),
                ('Bob Wilson', 'bob.wilson@unilorin.edu.ng', 'MTH', 'LC003')
            ]
            
            lecturers = {}
            for name, email, dept_code, lecturer_id in lecturers_data:
                lecturer = User(
                    id=lecturer_id,
                    name=name,
                    email=email,
                    role='lecturer',
                    department=departments[dept_code],
                    is_active=True
                )
                lecturer.set_password('Lecturer123!')
                lecturers[lecturer_id] = lecturer
                db.session.add(lecturer)
            
            # Create students
            students_data = [
                ('Alice Johnson', 'alice.j@unilorin.edu.ng', 'CSC', 'ST001'),
                ('Bob Brown', 'bob.b@unilorin.edu.ng', 'EEE', 'ST002'),
                ('Charlie Davis', 'charlie.d@unilorin.edu.ng', 'MTH', 'ST003')
            ]
            
            students = {}
            for name, email, dept_code, student_id in students_data:
                student = User(
                    id=student_id,
                    name=name,
                    email=email,
                    role='student',
                    department=departments[dept_code],
                    is_active=True
                )
                student.set_password('Student123!')
                students[student_id] = student
                db.session.add(student)
            
            # Create courses
            courses_data = [
                ('CSC101', 'Introduction to Computer Science', 'CSC', 'LC001'),
                ('CSC201', 'Data Structures and Algorithms', 'CSC', 'LC002'),
                ('MTH101', 'Calculus I', 'MTH', 'LC003')
            ]
            
            courses = {}
            for code, title, dept_code, lecturer_id in courses_data:
                course = Course(
                    code=code,
                    title=title,
                    department=departments[dept_code],
                    lecturer=lecturers[lecturer_id],
                    credits=3,
                    level='100',
                    semester=1,
                    is_active=True
                )
                courses[code] = course
                db.session.add(course)
            
            # Enroll students in courses
            enrollments = [
                ('ST001', 'CSC101'),
                ('ST001', 'MTH101'),
                ('ST002', 'CSC101'),
                ('ST003', 'MTH101')
            ]
            
            for student_id, course_code in enrollments:
                courses[course_code].enrolled_students.append(students[student_id])
            
            # Commit all changes
            db.session.commit()
            print("Database setup completed successfully!")
            
        except Exception as e:
            print(f"Error setting up database: {e}")
            db.session.rollback()

if __name__ == '__main__':
    # Remove the existing database file if it exists
    db_path = os.path.join('instance', 'attendance.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    setup_database()