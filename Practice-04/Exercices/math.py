#1. Write a Python program to convert degree to radian.

import math

degree = float(input("Input degree: "))

radian = math.radians(degree)

print("Output radian:", radian)

#2. Write a Python program to calculate the area of a trapezoid.

height = float(input("Height: "))
base_1 = float(input("Base, first value: "))
base_2 = float(input("Base, second value: "))

area = (base_1 + base_2) * height / 2

print("Area of trapezoid:", area)

#3. Write a Python program to calculate the area of regular polygon.

import math

n = int(input("Input number of sides: "))
side = float(input("Input the length of a side: "))

area = (n * side ** 2) / (4 * math.tan(math.pi / n))

print("The area of the polygon is:", area)

#4. Write a Python program to calculate the area of a parallelogram. 

base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))

area = base * height

print("Area of parallelogram:", area)
