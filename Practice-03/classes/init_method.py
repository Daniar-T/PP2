class Person:
    # __init__() assigns values when an object is created.
    def __init__(self, name, age):
        self.name = name
        self.age = age


# Create a Person object.
p1 = Person("Emil", 36)

print(p1.name)
print(p1.age)
