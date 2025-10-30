"""
University Course Registration System - Logic Layer
Implements OOP principles with Student, Course, and EnrollmentSystem classes
"""

import csv
import os


class Student:
    """Represents a student with student ID, name, and registered courses"""
    
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.registered_courses = set()
    
    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}"


class Course:
    """Represents a course with CRN, course ID, name, instructor, schedule, credits, and enrolled students"""
    
    def __init__(self, crn, course_id, name, instructor, schedule, credits, max_students=30):
        self.crn = crn  # Course Registration Number
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.schedule = schedule  # e.g., "MWF 10:00-11:00" or "TTh 14:00-15:30"
        self.credits = credits  # Credit hours
        self.enrolled_students = set()
        self.max_students = max_students
    
    def is_full(self):
        """Check if course has reached maximum capacity"""
        return len(self.enrolled_students) >= self.max_students
    
    def get_remaining_seats(self):
        """Get remaining seats in the course"""
        return self.max_students - len(self.enrolled_students)
    
    def get_days(self):
        """Extract days from schedule (e.g., 'MWF' from 'MWF 10:00-11:00')"""
        return self.schedule.split()[0] if ' ' in self.schedule else self.schedule
    
    def get_time(self):
        """Extract time from schedule (e.g., '10:00-11:00' from 'MWF 10:00-11:00')"""
        parts = self.schedule.split()
        return parts[1] if len(parts) > 1 else ""
    
    def __str__(self):
        return f"CRN {self.crn}: {self.course_id} - {self.name} ({self.credits} credits)"


class EnrollmentSystem:
    """Manages student-course registrations and maintains records"""
    
    def __init__(self):
        self.students = {}  # Dictionary: student_id -> Student object
        self.courses = {}   # Dictionary: crn -> Course object
        self.course_by_id = {}  # Dictionary: course_id -> Course object for lookup
        self.load_data()
        self.initialize_courses()  # Pre-load Spring 2026 courses
        self.initialize_dummy_students()  # Add dummy student data
    
    def initialize_courses(self):
        """Initialize Spring 2026 courses if not already loaded"""
        if not self.courses:
            # Spring 2026 Course Catalog
            # Format: (CRN, CourseID, Name, Instructor, Schedule, Credits, Capacity)
            spring_courses = [
                (10001, "CS101", "Introduction to Computer Science", "Dr. Smith", "MWF 09:00-10:00", 3, 30),
                (10002, "CS102", "Data Structures", "Dr. Johnson", "TTh 10:00-11:30", 4, 30),
                (10003, "CS201", "Algorithms", "Dr. Williams", "MWF 11:00-12:00", 3, 25),
                (10004, "CS202", "Database Systems", "Dr. Brown", "TTh 14:00-15:30", 3, 30),
                (10005, "CS301", "Operating Systems", "Dr. Davis", "MWF 14:00-15:00", 4, 25),
                (10006, "MATH101", "Calculus I", "Prof. Miller", "MWF 08:00-09:00", 4, 35),
                (10007, "MATH102", "Linear Algebra", "Prof. Taylor", "TTh 09:00-10:30", 3, 30),
                (10008, "PHYS101", "Physics I", "Dr. Wilson", "MWF 13:00-14:00", 4, 30),
                (10009, "PHYS102", "Physics II", "Dr. Moore", "TTh 11:00-12:30", 4, 25),
                (10010, "ENG101", "English Composition", "Prof. Anderson", "MWF 10:00-11:00", 3, 25),
                (10011, "ENG201", "Technical Writing", "Prof. Thomas", "TTh 13:00-14:30", 3, 25),
                (10012, "HIST101", "World History", "Dr. Jackson", "MWF 15:00-16:00", 3, 30),
                (10013, "BIO101", "Biology I", "Dr. White", "TTh 08:00-09:30", 4, 30),
                (10014, "CHEM101", "Chemistry I", "Dr. Harris", "MWF 12:00-13:00", 4, 28),
                (10015, "ECON101", "Microeconomics", "Prof. Martin", "TTh 15:30-17:00", 3, 30),
            ]
            
            for crn, course_id, name, instructor, schedule, credits, capacity in spring_courses:
                course = Course(crn, course_id, name, instructor, schedule, credits, capacity)
                self.courses[crn] = course
                self.course_by_id[course_id] = course
            
            self.save_data()
    
    def initialize_dummy_students(self):
        """Add dummy students with pre-enrolled courses"""
        if len(self.students) == 0:
            # Create dummy students
            dummy_students = [
                ("S1001", "Alice Johnson"),
                ("S1002", "Bob Smith"),
                ("S1003", "Charlie Brown"),
            ]
            
            for student_id, name in dummy_students:
                if student_id not in self.students:
                    self.students[student_id] = Student(student_id, name)
            
            # Pre-enroll Alice in some courses
            if "S1001" in self.students:
                alice_courses = [10001, 10006, 10010]  # CS101, MATH101, ENG101 (10 credits)
                for crn in alice_courses:
                    if crn in self.courses:
                        self.students["S1001"].registered_courses.add(crn)
                        self.courses[crn].enrolled_students.add("S1001")
            
            # Pre-enroll Bob in some courses
            if "S1002" in self.students:
                bob_courses = [10002, 10007, 10013]  # CS102, MATH102, BIO101 (11 credits)
                for crn in bob_courses:
                    if crn in self.courses:
                        self.students["S1002"].registered_courses.add(crn)
                        self.courses[crn].enrolled_students.add("S1002")
            
            self.save_data()
    
    def has_schedule_conflict(self, student_id, new_crn):
        """
        Check if enrolling in new course would create a schedule conflict
        Returns: (has_conflict: bool, conflicting_course: Course or None)
        """
        if student_id not in self.students or new_crn not in self.courses:
            return False, None
        
        student = self.students[student_id]
        new_course = self.courses[new_crn]
        new_days = set(new_course.get_days())
        new_time = new_course.get_time()
        
        for crn in student.registered_courses:
            if crn in self.courses:
                existing_course = self.courses[crn]
                existing_days = set(existing_course.get_days())
                existing_time = existing_course.get_time()
                
                # Check if there's any day overlap
                if new_days & existing_days:
                    # Check if times overlap
                    if self.times_overlap(new_time, existing_time):
                        return True, existing_course
        
        return False, None
    
    def times_overlap(self, time1, time2):
        """Check if two time ranges overlap"""
        if not time1 or not time2:
            return False
        
        try:
            # Parse time ranges like "10:00-11:00"
            start1, end1 = time1.split('-')
            start2, end2 = time2.split('-')
            
            # Convert to minutes for comparison
            start1_min = self.time_to_minutes(start1)
            end1_min = self.time_to_minutes(end1)
            start2_min = self.time_to_minutes(start2)
            end2_min = self.time_to_minutes(end2)
            
            # Check overlap
            return not (end1_min <= start2_min or end2_min <= start1_min)
        except:
            return False
    
    def time_to_minutes(self, time_str):
        """Convert time string like '10:00' to minutes"""
        hours, minutes = map(int, time_str.strip().split(':'))
        return hours * 60 + minutes
    
    def get_student_total_credits(self, student_id):
        """Calculate total credit hours for a student"""
        if student_id not in self.students:
            return 0
        
        student = self.students[student_id]
        total_credits = 0
        for crn in student.registered_courses:
            if crn in self.courses:
                total_credits += self.courses[crn].credits
        return total_credits
    
    def load_data(self):
        """Load student and course data from CSV files"""
        # Load students from students.csv
        if os.path.exists('students.csv'):
            try:
                with open('students.csv', 'r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    next(reader, None)  # Skip header
                    for row in reader:
                        if len(row) >= 2:
                            student_id, name = row[0], row[1]
                            student = Student(student_id, name)
                            # Load registered courses (CRNs) if present
                            if len(row) > 2 and row[2]:
                                courses_str = row[2]
                                if courses_str:
                                    # Convert string CRNs to integers
                                    student.registered_courses = set(int(crn) for crn in courses_str.split(';') if crn.strip().isdigit())
                            self.students[student_id] = student
            except Exception as e:
                print(f"Error loading students: {e}")
        
        # Load courses from courses.csv
        if os.path.exists('courses.csv'):
            try:
                with open('courses.csv', 'r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    next(reader, None)  # Skip header
                    for row in reader:
                        if len(row) >= 6:
                            crn = int(row[0])
                            course_id, name, instructor, schedule = row[1], row[2], row[3], row[4]
                            credits = int(row[5]) if row[5] else 3
                            max_students = int(row[6]) if len(row) > 6 and row[6] else 30
                            course = Course(crn, course_id, name, instructor, schedule, credits, max_students)
                            # Load enrolled students if present
                            if len(row) > 7 and row[7]:
                                students_str = row[7]
                                if students_str:
                                    course.enrolled_students = set(students_str.split(';'))
                            self.courses[crn] = course
                            self.course_by_id[course_id] = course
            except Exception as e:
                print(f"Error loading courses: {e}")
        
        # Load enrollments from enrollments.csv
        if os.path.exists('enrollments.csv'):
            try:
                with open('enrollments.csv', 'r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    next(reader, None)  # Skip header
                    for row in reader:
                        if len(row) >= 2:
                            student_id = row[0]
                            crn = int(row[1]) if row[1].isdigit() else None
                            if crn and student_id in self.students and crn in self.courses:
                                self.students[student_id].registered_courses.add(crn)
                                self.courses[crn].enrolled_students.add(student_id)
            except Exception as e:
                print(f"Error loading enrollments: {e}")
    
    def save_data(self):
        """Save all data to CSV files"""
        # Save students to students.csv
        try:
            with open('students.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['student_id', 'name', 'registered_courses'])
                for student in self.students.values():
                    courses_str = ';'.join(str(crn) for crn in student.registered_courses)
                    writer.writerow([student.student_id, student.name, courses_str])
        except Exception as e:
            print(f"Error saving students: {e}")
        
        # Save courses to courses.csv
        try:
            with open('courses.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['crn', 'course_id', 'name', 'instructor', 'schedule', 'credits', 'max_students', 'enrolled_students'])
                for course in self.courses.values():
                    students_str = ';'.join(course.enrolled_students)
                    writer.writerow([course.crn, course.course_id, course.name, course.instructor, 
                                   course.schedule, course.credits, course.max_students, students_str])
        except Exception as e:
            print(f"Error saving courses: {e}")
        
        # Save enrollments to enrollments.csv
        try:
            with open('enrollments.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['student_id', 'crn'])
                for student in self.students.values():
                    for crn in student.registered_courses:
                        writer.writerow([student.student_id, crn])
        except Exception as e:
            print(f"Error saving enrollments: {e}")
    
    def register_student(self, student_id, name):
        """
        Register a new student account
        Returns: (success: bool, message: str)
        """
        try:
            if not student_id or not name:
                return False, "Student ID and name are required"
            
            if student_id in self.students:
                return False, f"Student ID {student_id} already exists"
            
            student = Student(student_id, name)
            self.students[student_id] = student
            self.save_data()
            return True, f"Student {name} registered successfully"
        except Exception as e:
            return False, f"Error registering student: {str(e)}"
    

    
    def enroll_student(self, student_id, crn):
        """
        Enroll a student in a course using CRN (prevents schedule conflicts and enforces credit limit)
        Returns: (success: bool, message: str)
        """
        try:
            # Convert CRN to integer
            try:
                crn = int(crn)
            except ValueError:
                return False, "Invalid CRN. Please enter a numeric CRN."
            
            # Validate student exists
            if student_id not in self.students:
                return False, "Student not found. Please register first."
            
            # Validate course exists
            if crn not in self.courses:
                return False, f"Course with CRN {crn} not found"
            
            student = self.students[student_id]
            course = self.courses[crn]
            
            # Check if already enrolled
            if crn in student.registered_courses:
                return False, f"Already enrolled in {course.name}"
            
            # Check course capacity
            if course.is_full():
                return False, f"Course {course.name} is full (max: {course.max_students})"
            
            # Check credit hour limit (18 credits max)
            current_credits = self.get_student_total_credits(student_id)
            if current_credits + course.credits > 18:
                return False, f"Cannot enroll: Would exceed 18 credit hour limit (Current: {current_credits}, Course: {course.credits})"
            
            # Check for schedule conflicts
            has_conflict, conflicting_course = self.has_schedule_conflict(student_id, crn)
            if has_conflict:
                return False, f"Schedule conflict with CRN {conflicting_course.crn}: {conflicting_course.course_id} - {conflicting_course.name}"
            
            # Enroll the student
            student.registered_courses.add(crn)
            course.enrolled_students.add(student_id)
            self.save_data()
            
            new_total = current_credits + course.credits
            return True, f"Successfully enrolled in {course.name} ({course.credits} credits)\nTotal credits: {new_total}/18"
        except Exception as e:
            return False, f"Error enrolling student: {str(e)}"
    
    def drop_course(self, student_id, crn):
        """
        Drop a student from a course using CRN
        Returns: (success: bool, message: str)
        """
        try:
            # Convert CRN to integer
            try:
                crn = int(crn)
            except ValueError:
                return False, "Invalid CRN"
            
            # Validate student exists
            if student_id not in self.students:
                return False, "Student not found"
            
            # Validate course exists
            if crn not in self.courses:
                return False, f"Course with CRN {crn} not found"
            
            student = self.students[student_id]
            course = self.courses[crn]
            
            # Check if enrolled
            if crn not in student.registered_courses:
                return False, f"Not enrolled in {course.name}"
            
            # Drop the course
            student.registered_courses.remove(crn)
            course.enrolled_students.remove(student_id)
            self.save_data()
            
            new_total = self.get_student_total_credits(student_id)
            return True, f"Dropped from {course.name} ({course.credits} credits)\nTotal credits: {new_total}/18"
        except Exception as e:
            return False, f"Error dropping course: {str(e)}"
    
    def view_available_courses(self):
        """
        Get list of all available courses
        Returns: list of Course objects sorted by CRN
        """
        return sorted(self.courses.values(), key=lambda c: c.crn)
    
    def get_student_courses(self, student_id):
        """
        Get courses a student is enrolled in
        Returns: list of Course objects
        """
        if student_id not in self.students:
            return []
        
        student = self.students[student_id]
        return [self.courses[crn] for crn in student.registered_courses if crn in self.courses]
    
    def get_all_students(self):
        """Get list of all students"""
        return list(self.students.values())
    
    def get_student(self, student_id):
        """Get a specific student"""
        return self.students.get(student_id)
