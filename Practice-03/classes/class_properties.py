class Person:
    def __init__(self, name, age):
        # Create instance variables for this object.
        self.name = name
        self.age = age
# Create a Person object.
p1 = Person("Linus", 30)
# Delete only the age property from p1.
del p1.age
# name still exists, so this works.
print(p1.name) # This works
# print(p1.age) # This would cause an error 
