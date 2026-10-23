def create_student():
    name = input("Enter student name: ").strip()
    age = int(input("Enter student age: "))
    student_id = input("Enter student ID: ").strip()
    grade = input("Enter student grade: ").strip()

    student = {
        "name": name,
        "age": age,
        "student_id": student_id,
        "grade": grade
    }

    print("Student created successfully!")
    return student

create_student()