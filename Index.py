DB = []
names = []
grades = []
category = []


# Agrawal
def categorization(marks):
    pass


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
def validateGrade():
    pass


# test case needed
userInteraction()


# additional functions
"""
def displayUsers():
    pass

def deleteUsers():
    pass
    
"""
