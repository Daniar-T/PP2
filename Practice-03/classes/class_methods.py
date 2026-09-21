class Person:
    def __init__(self, name, age):
        # self refers to the current object.
        # Store name and age in that object.
        self.name = name
        self.age = age
    def greet(self):
        # self.name accesses the name belonging to this object.
        print("Hello, my name is " + self.name)
# Create a Person object.
p1 = Person("Emil", 25)
# Call the greet() method for p1.
p1.greet()
