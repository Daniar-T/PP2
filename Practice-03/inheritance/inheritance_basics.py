class Person:
    # Define the constructor method
    def __init__(self, fname, lname):
        self.firstname = fname  # Define an instance variable
        self.lastname = lname  # Define an instance variable
    # Define a method to print the full name
    def printname(self):
        print(self.firstname, self.lastname)  # Print the first and last name
class Student(Person):
    pass  # Inherit the Person class without adding new features
x = Student("Mike", "Olsen")  # Create a Student object
x.printname()  # Call the inherited printname method
