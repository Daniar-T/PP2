numbers = [1, 2, 3, 4, 5]
# map() applies the lambda function to every item in numbers
# The lambda receives one number at a time and multiplies it by 2
doubled = list(map(lambda x: x * 2, numbers))   # map() produces a map object, so list() converts the results into a list
print(doubled)                                  # Print the new list

#Output: [2, 4, 6, 8, 10]