class MyClass:
    # x is a class variable.
    # It belongs to MyClass and is shared by objects created from it.
    x = 5
# Print the class itself.
# This displays information about the class, not the value of x.
print(MyClass)
# Create an object from MyClass.
# p1 is an instance, or object, of MyClass.
p1 = MyClass()
# Access the class variable through the object.
print(p1.x)

#Output: 5