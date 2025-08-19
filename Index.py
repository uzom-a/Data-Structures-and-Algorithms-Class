DB = []
names = []
grades = []
category = []


# Agrawal
def categorization(marks):
    
    if marks < 70:
        return "Needs Improvement"
    elif marks < 80:
        return "Average"
    elif marks < 90:
        return "Good"
    else:
        return "Excellent"


# Uzoma
def userInteraction():
    name = input("Enter the student's name: ")
    grade = int(input("Enter the student's grade: "))


# Kelvin
def saveUser(name, grade, classification):
    try:
        if len(names) < 10:
            names.append(name)
        else:
            raise Exception("Database already has names of 10 students")

    except Exception as failed:
        print("Error", failed)

    try:
        if len(grades) < 10:
            grade.append(grade)
        else:
            raise Exception("Database already has grade of 10 students")

    except Exception as Error:
        print("Error", Error)

    try:
        if len(category) < 10:
            category.append(classification)
        else:
            raise Exception(
                "Cannot classify student grade as the limit of 10 students have been reached"
            )

    except Exception as mistake:
        print("Error", mistake)

    # pass


# Agrawal
def validateGrade(grade):
    if grade > 100 or grade < 0:
        return False
    return True
    


def main():
    print("------------------------------------")
    print("Welcome to Student Portal")
    print("------------------------------------")

    print("What task you want to perform: ")
    print("Create - Create Student")
    print("DELETE - Delete Student")
    print("VIEW - View Student")
    print("VIEWALL - View all Student Records")
    



    userInteraction()

main()

# test case needed


# additional functions and display the average, maximum and minimum
"""
def displayUsers():
    pass

def deleteUsers():
    pass
    
"""
