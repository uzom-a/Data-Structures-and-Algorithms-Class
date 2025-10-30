"""
University Course Registration System - GUI
Student-focused interface for Spring 2026 course registration
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from registration_logic import EnrollmentSystem


class RegistrationGUI:
    """Main GUI application for Student Course Registration"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("University Course Registration - Spring 2026")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Initialize the enrollment system
        self.system = EnrollmentSystem()
        self.current_student_id = None
        
        # Show login screen first
        self.show_login_screen()
    
    def show_login_screen(self):
        """Display login/registration screen"""
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(fill='both', expand=True, padx=50, pady=50)
        
        # Title
        title = ttk.Label(self.login_frame, text="University Course Registration System", 
                         font=('Arial', 18, 'bold'))
        title.pack(pady=20)
        
        subtitle = ttk.Label(self.login_frame, text="Spring 2026", 
                           font=('Arial', 14))
        subtitle.pack(pady=5)
        
        # Login section
        login_section = ttk.LabelFrame(self.login_frame, text="Student Login", padding=20)
        login_section.pack(pady=30, fill='x')
        
        ttk.Label(login_section, text="Student ID:").grid(row=0, column=0, padx=5, pady=10, sticky='e')
        self.login_id_entry = ttk.Entry(login_section, width=30)
        self.login_id_entry.grid(row=0, column=1, padx=5, pady=10)
        
        login_btn = ttk.Button(login_section, text="Login", command=self.login)
        login_btn.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Registration section
        register_section = ttk.LabelFrame(self.login_frame, text="New Student Registration", padding=20)
        register_section.pack(pady=20, fill='x')
        
        ttk.Label(register_section, text="Student ID:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.reg_id_entry = ttk.Entry(register_section, width=30)
        self.reg_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(register_section, text="Full Name:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.reg_name_entry = ttk.Entry(register_section, width=30)
        self.reg_name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        register_btn = ttk.Button(register_section, text="Register New Account", command=self.register_new_student)
        register_btn.grid(row=2, column=0, columnspan=2, pady=10)
    
    def login(self):
        """Login with existing student ID"""
        student_id = self.login_id_entry.get().strip()
        
        if not student_id:
            messagebox.showerror("Error", "Please enter your Student ID")
            return
        
        student = self.system.get_student(student_id)
        if not student:
            messagebox.showerror("Error", "Student ID not found. Please register first.")
            return
        
        self.current_student_id = student_id
        self.login_frame.destroy()
        self.show_main_interface()
    
    def register_new_student(self):
        """Register a new student account"""
        student_id = self.reg_id_entry.get().strip()
        name = self.reg_name_entry.get().strip()
        
        success, message = self.system.register_student(student_id, name)
        
        if success:
            messagebox.showinfo("Success", message)
            self.current_student_id = student_id
            self.login_frame.destroy()
            self.show_main_interface()
        else:
            messagebox.showerror("Error", message)
    
    def show_main_interface(self):
        """Display main course registration interface"""
        student = self.system.get_student(self.current_student_id)
        
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=10, pady=10)
        
        welcome_label = ttk.Label(header_frame, 
                                  text=f"Welcome, {student.name} ({student.student_id})",
                                  font=('Arial', 14, 'bold'))
        welcome_label.pack(side='left')
        
        logout_btn = ttk.Button(header_frame, text="Logout", command=self.logout)
        logout_btn.pack(side='right')
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_view_courses_tab()
        self.create_enroll_tab()
        self.create_my_schedule_tab()
    
    def logout(self):
        """Logout and return to login screen"""
        self.current_student_id = None
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_login_screen()
    
    def create_view_courses_tab(self):
        """Tab for viewing all available Spring 2026 courses"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Available Courses")
        
        # Title
        title = ttk.Label(frame, text="Spring 2026 Course Catalog", font=('Arial', 16, 'bold'))
        title.pack(pady=20)
        
        # Filter frame
        filter_frame = ttk.LabelFrame(frame, text="Filter by Subject", padding=10)
        filter_frame.pack(pady=10, padx=20, fill='x')
        
        # Subject dropdown
        ttk.Label(filter_frame, text="Select Subject:", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        self.subject_var = tk.StringVar(value="All Subjects")
        subjects = ["All Subjects", "Computer Science", "Mathematics", "Physics", "Chemistry", 
                   "Biology", "English", "History", "Economics"]
        self.subject_dropdown = ttk.Combobox(filter_frame, textvariable=self.subject_var, 
                                            values=subjects, state='readonly', width=25, font=('Arial', 10))
        self.subject_dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        # Search button
        search_btn = ttk.Button(filter_frame, text="Search Courses", command=self.search_courses)
        search_btn.grid(row=0, column=2, padx=10, pady=5)
        
        # Clear filter button
        clear_btn = ttk.Button(filter_frame, text="Show All", command=self.clear_filter)
        clear_btn.grid(row=0, column=3, padx=5, pady=5)
        
        # Courses display
        self.courses_display = scrolledtext.ScrolledText(frame, height=25, width=95, font=('Courier', 10))
        self.courses_display.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Initial load
        self.refresh_courses()
    
    def create_enroll_tab(self):
        """Tab for enrolling in courses"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Enroll in Course")
        
        # Title
        title = ttk.Label(frame, text="Course Enrollment", font=('Arial', 16, 'bold'))
        title.pack(pady=20)
        
        # Credit info
        self.credit_info_label = ttk.Label(frame, text="", font=('Arial', 11, 'bold'), foreground='blue')
        self.credit_info_label.pack(pady=5)
        self.update_credit_info()
        
        # Input frame
        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="CRN:", font=('Arial', 11, 'bold')).grid(row=0, column=0, padx=5, pady=10, sticky='e')
        self.enroll_crn = ttk.Entry(input_frame, width=20, font=('Arial', 11))
        self.enroll_crn.grid(row=0, column=1, padx=5, pady=10)
        
        ttk.Label(input_frame, text="(e.g., 10001, 10002)", font=('Arial', 9, 'italic')).grid(row=1, column=1, sticky='w')
        
        # Enroll button
        enroll_btn = ttk.Button(frame, text="Enroll Using CRN", command=self.enroll_in_course)
        enroll_btn.pack(pady=10)
        
        # Status display
        ttk.Label(frame, text="Enrollment Status:", font=('Arial', 11, 'bold')).pack(pady=(20,5))
        self.enrollment_status = scrolledtext.ScrolledText(frame, height=20, width=80, font=('Courier', 10))
        self.enrollment_status.pack(pady=10, padx=20)
    
    def update_credit_info(self):
        """Update the credit information display"""
        if self.current_student_id:
            total_credits = self.system.get_student_total_credits(self.current_student_id)
            self.credit_info_label.config(text=f"Current Credit Hours: {total_credits}/18")

    
    def create_my_schedule_tab(self):
        """Tab for viewing and managing enrolled courses"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="My Schedule")
        
        # Title
        title = ttk.Label(frame, text="My Course Schedule", font=('Arial', 16, 'bold'))
        title.pack(pady=20)
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        refresh_btn = ttk.Button(btn_frame, text="Refresh Schedule", command=self.refresh_schedule)
        refresh_btn.grid(row=0, column=0, padx=5)
        
        drop_btn = ttk.Button(btn_frame, text="Drop Selected Course", command=self.drop_course_dialog)
        drop_btn.grid(row=0, column=1, padx=5)
        
        # Schedule display
        self.schedule_display = scrolledtext.ScrolledText(frame, height=25, width=90, font=('Courier', 10))
        self.schedule_display.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Initial load
        self.refresh_schedule()
    
    def refresh_courses(self, filtered_courses=None):
        """Refresh the courses display"""
        self.courses_display.delete('1.0', tk.END)
        
        if filtered_courses is None:
            courses = self.system.view_available_courses()
        else:
            courses = filtered_courses
        
        # Header
        self.courses_display.insert('1.0', "=" * 95 + "\n")
        if filtered_courses is None:
            self.courses_display.insert(tk.END, "SPRING 2026 COURSE CATALOG - ALL COURSES\n")
        else:
            subject = self.subject_var.get()
            self.courses_display.insert(tk.END, f"SPRING 2026 COURSE CATALOG - {subject.upper()}\n")
        self.courses_display.insert(tk.END, "=" * 95 + "\n\n")
        
        if courses:
            self.courses_display.insert(tk.END, f"Found {len(courses)} course(s)\n\n")
            
            # Course listing
            for course in courses:
                remaining = course.get_remaining_seats()
                status = "FULL" if course.is_full() else f"{remaining} seats available"
                
                self.courses_display.insert(tk.END, 
                    f"CRN: {course.crn}  |  {course.course_id}  |  {course.name}\n"
                    f"   Instructor: {course.instructor}\n"
                    f"   Schedule:   {course.schedule}\n"
                    f"   Credits:    {course.credits} credit hours\n"
                    f"   Capacity:   {len(course.enrolled_students)}/{course.max_students} enrolled - {status}\n\n")
        else:
            self.courses_display.insert(tk.END, "No courses found matching your criteria.\n")
    
    def search_courses(self):
        """Filter courses by selected subject"""
        subject = self.subject_var.get()
        
        if subject == "All Subjects":
            self.refresh_courses()
            return
        
        # Get all courses
        all_courses = self.system.view_available_courses()
        
        # Define subject mapping
        subject_mapping = {
            "Computer Science": ["CS"],
            "Mathematics": ["MATH"],
            "Physics": ["PHYS"],
            "Chemistry": ["CHEM"],
            "Biology": ["BIO"],
            "English": ["ENG"],
            "History": ["HIST"],
            "Economics": ["ECON"]
        }
        
        # Filter courses by subject prefix
        prefixes = subject_mapping.get(subject, [])
        filtered = [course for course in all_courses 
                   if any(course.course_id.startswith(prefix) for prefix in prefixes)]
        
        self.refresh_courses(filtered)
    
    def clear_filter(self):
        """Clear the filter and show all courses"""
        self.subject_var.set("All Subjects")
        self.refresh_courses()
    
    def enroll_in_course(self):
        """Enroll the current student in a course using CRN"""
        crn = self.enroll_crn.get().strip()
        
        if not crn:
            messagebox.showerror("Error", "Please enter a CRN")
            return
        
        success, message = self.system.enroll_student(self.current_student_id, crn)
        
        if success:
            self.enrollment_status.insert('1.0', f"✓ {message}\n\n")
            self.enroll_crn.delete(0, tk.END)
            messagebox.showinfo("Success", message)
            self.refresh_schedule()
            self.update_credit_info()
        else:
            self.enrollment_status.insert('1.0', f"✗ {message}\n\n")
            messagebox.showerror("Error", message)
    
    def refresh_schedule(self):
        """Refresh the student's schedule"""
        self.schedule_display.delete('1.0', tk.END)
        
        student = self.system.get_student(self.current_student_id)
        courses = self.system.get_student_courses(self.current_student_id)
        total_credits = self.system.get_student_total_credits(self.current_student_id)
        
        # Header
        self.schedule_display.insert('1.0', "=" * 95 + "\n")
        self.schedule_display.insert(tk.END, f"MY SCHEDULE - {student.name} ({student.student_id})\n")
        self.schedule_display.insert(tk.END, "=" * 95 + "\n\n")
        
        if courses:
            self.schedule_display.insert(tk.END, f"Total Courses: {len(courses)}  |  Total Credits: {total_credits}/18\n\n")
            
            for course in sorted(courses, key=lambda c: c.crn):
                self.schedule_display.insert(tk.END, 
                    f"CRN: {course.crn}  |  {course.course_id}  |  {course.name}\n"
                    f"   Instructor: {course.instructor}\n"
                    f"   Schedule:   {course.schedule}\n"
                    f"   Credits:    {course.credits} credit hours\n\n")
        else:
            self.schedule_display.insert(tk.END, "No courses enrolled yet.\n")
            self.schedule_display.insert(tk.END, "Visit the 'Enroll in Course' tab to add courses.\n")
    
    def drop_course_dialog(self):
        """Show dialog to drop a course"""
        student = self.system.get_student(self.current_student_id)
        courses = self.system.get_student_courses(self.current_student_id)
        
        if not courses:
            messagebox.showinfo("Info", "You are not enrolled in any courses.")
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Drop Course")
        dialog.geometry("500x350")
        
        ttk.Label(dialog, text="Select course to drop:", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Listbox for course selection
        listbox = tk.Listbox(dialog, height=10, font=('Arial', 10))
        listbox.pack(pady=10, padx=20, fill='both', expand=True)
        
        for course in courses:
            listbox.insert(tk.END, f"CRN {course.crn} - {course.course_id}: {course.name} ({course.credits} credits)")
        
        def drop_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "Please select a course")
                return
            
            crn = courses[selection[0]].crn
            success, message = self.system.drop_course(self.current_student_id, crn)
            
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.refresh_schedule()
                self.update_credit_info()
            else:
                messagebox.showerror("Error", message)
        
        ttk.Button(dialog, text="Drop Course", command=drop_selected).pack(pady=10)


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = RegistrationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
