names = []
grades = []
categories = []
student_ids = []
global_id = 1


def categorize_grade(marks):
    if marks < 70:
        return "Needs Improvement"
    elif marks < 80:
        return "Average"
    elif marks < 90:
        return "Good"
    else:
        return "Excellent"


def validate_grade(grade):
    return 0 <= grade <= 100


def add_student():
    global global_id
    if len(names) >= 10:
        print("Cannot add more students. Limit of 10 reached.")
        return
    name = input("Enter the student's name: ").strip()
    try:
        grade = int(input("Enter the student's grade (0-100): "))
    except ValueError:
        print("Invalid input. Grade must be an integer.")
        return
    if not validate_grade(grade):
        print("Grade must be between 0 and 100.")
        return
    category = categorize_grade(grade)
    names.append(name)
    grades.append(grade)
    categories.append(category)
    student_ids.append(global_id)
    print(f"Student '{name}' added successfully.")
    global_id += 1


def display_students():
    if not names:
        print("No student records to display.")
        return
    print("\n{:<5} {:<15} {:<7} {:<18}".format("ID", "Name", "Grade", "Category"))
    print("-" * 45)
    for i in range(len(names)):
        print(
            "{:<5} {:<15} {:<7} {:<18}".format(
                student_ids[i], names[i], grades[i], categories[i]
            )
        )
    print("-" * 45)
    print(f"Average Grade: {average_grade():.2f}")
    print(f"Maximum Grade: {max_grade()}")
    print(f"Minimum Grade: {min_grade()}")


def average_grade():
    return sum(grades) / len(grades) if grades else 0


def max_grade():
    return max(grades) if grades else 0


def min_grade():
    return min(grades) if grades else 0


def delete_student():
    if not names:
        print("No students to delete.")
        return
    try:
        sid = int(input("Enter the student ID to delete: "))
    except ValueError:
        print("Invalid input. ID must be an integer.")
        return
    if sid in student_ids:
        idx = student_ids.index(sid)
        print(f"Deleting student: {names[idx]}")
        del names[idx]
        del grades[idx]
        del categories[idx]
        del student_ids[idx]
        print("Student deleted successfully.")
    else:
        print("Student ID not found.")


def main():
    print("------------------------------------")
    print("Welcome to Student Portal")
    print("------------------------------------")
    while True:
        print("\nSelect an option:")
        print("1 - Add Student")
        print("2 - View All Students")
        print("3 - Delete Student")
        print("4 - Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_student()
        elif choice == "2":
            display_students()
        elif choice == "3":
            delete_student()
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()
