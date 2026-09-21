students = [
    ("Emil", 25),
    ("Tobias", 22),
    ("Linus", 28)
]

# sorted() sorts the items in the students list
# key= tells sorted() which value to use for sorting

# The lambda receives one tuple at a time:
# ("Emil", 25), ("Tobias", 22), or ("Linus", 28)

# x[1] selects the second item in each tuple:
# "Emil", 25    -> 25
# "Tobias", 22  -> 22
# "Linus", 28   -> 28

# The students are sorted by age
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)                                      # Print the sorted list

#Output: [('Tobias', 22), ('Emil', 25), ('Linus', 28)]