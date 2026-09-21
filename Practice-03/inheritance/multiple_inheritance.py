class Person:
    # Define the person's name
    def __init__(self, name):
        self.name = name  # Store the name
class Employee:
    # Define the employee's job
    def work(self):
        print(self.name, "is working")  # Print the work message
class Student(Person, Employee):
    pass  # Inherit from both Person and Employee
x = Student("Mike")  # Create a Student object
x.work()  # Call the inherited method
