# no option to add after limit reached (Kelvin)
# directly able to edit the name and grade (Dharambir)
# not accepting numbers as name (Kelvin) ***
# add count for the number of student to add (Dharambir)
# display number of student added already (Kelvin)
# no option for deleting student at the beginning (uzoma)

names = []
grades = []
categories = []
student_ids = []
global_id = 1


# Dharambir
def categorize_grade(marks):
    if marks < 70:
        return "Needs Improvement"
    elif marks < 80:
        return "Average"
    elif marks < 90:
        return "Good"
    else:
        return "Excellent"


# Dharambir
def validate_grade(grade):
    return 0 <= grade <= 100

# Dharambir

def input_name():
    while True:
        name = input("Enter the student's name: ").strip()

        # Check if name is empty after stripping spaces
        if not name:
            print("Name cannot be empty or only spaces.")
            continue

        # Check if name is made up of only digits
        if name.replace(" ", "").isdigit():
            print("Name cannot be numbers only.")
            continue

        # Check if all characters are letters, digits, or spaces
        valid = True
        for char in name:
            if not (char.isalnum() or char.isspace()):
                valid = False
                break

        if valid:
            break
        else:
            print("Invalid name. Only letters, numbers, and spaces are allowed.")
    return name



# Uzoma
def add_student():
    global global_id
    # validating the name
    name = input_name()
    # while True:
    #     name = input("Enter the student's name: ").strip()
    #     if all(part.isalpha() for part in name.split()):
    #         break
    #     else:
    #         print("Invalid input. Name must contain only letters and spaces")
    # validating the grade
    while True:
        try:
            grade = int(input("Enter the student's grade (0-100): "))
            if not validate_grade(grade):
                print("Grade must be between 0 and 100.")
            else:
                break
        except ValueError:
            print("Invalid input. Grade must be an integer.")
            # return

        # return
    category = categorize_grade(grade)
    names.append(name)
    grades.append(grade)
    categories.append(category)
    student_ids.append(global_id)
    print(f"Student '{name}' added successfully.")
    global_id += 1


# Kelvin
def display_students():
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


# Dharambir
def average_grade():
    return sum(grades) / len(grades) if grades else 0


# Dharambir
def max_grade():
    return max(grades) if grades else 0


# Dharambir
def min_grade():
    return min(grades) if grades else 0


# Uzoma
def delete_student():
    if not names:
        print("No students to delete.")
        return

    # Display current students for reference
    print("\nCurrent Students:")
    print("{:<5} {:<15}".format("ID", "Name"))
    print("-" * 20)
    for i in range(len(names)):
        print("{:<5} {:<15}".format(student_ids[i], names[i]))
    print("-" * 20)

    # Persistent validation for student ID
    while True:
        try:
            sid = int(input("Enter the student ID to delete: "))
            if sid in student_ids:
                idx = student_ids.index(sid)
                print(f"Deleting student: {names[idx]}")
                del names[idx]
                del grades[idx]
                del categories[idx]
                del student_ids[idx]
                print("Student deleted successfully.\n")
                break
            else:
                print(
                    "Student ID not found. Please enter a valid ID from the list above."
                )
        except ValueError:
            print("Invalid input. ID must be an integer. Please try again.")


# Kelvin - Main program and menu system
def main():
    print("------------------------------------")
    print("Welcome to Student Portal")
    print("------------------------------------")
    while True:

        print(f"\n{len(names)} students added")
        print(f"There are {(10 - len(names))} more name(s) to add")
        print("Select an option:")
        if len(names) < 10:
            print("1 - Add Student")
        if len(names) > 0:
            print("2 - View All Students")
        if names:
            print("3 - Delete Student")
        print("4 - Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            if len(names) >= 10:
                print("Cannot add more students. Limit of 10 reached.")
            else:
                a = input(
                    f"How many student(s) you want to add between 1 and {10 - len(names)}: "
                )
                try:
                    num_students = int(a)
                    if 1 <= num_students <= (10 - len(names)):
                        for _ in range(num_students):
                            add_student()
                    else:
                        print(
                            f"Invalid number. Please enter a number between 1 and {10 - len(names)}."
                        )
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
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
