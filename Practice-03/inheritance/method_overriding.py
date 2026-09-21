class Person:
    # Define the constructor method
    def __init__(self, fname, lname):
        self.firstname = fname  # Define the first-name variable
        self.lastname = lname  # Define the last-name variable
    # Define the parent-class method
    def printname(self):
        print(self.firstname, self.lastname)  # Print the name
class Student(Person):
    # Override the printname method
    def printname(self):
        print(
            "Student:",
            self.firstname,
            self.lastname
        )  # Print the name with different text
x = Student("Mike", "Olsen")  # Create a Student object
x.printname()  # Call the overridden method
