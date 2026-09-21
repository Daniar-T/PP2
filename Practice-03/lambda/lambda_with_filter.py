numbers = [1, 2, 3, 4, 5, 6, 7, 8]
# filter() checks every item in the numbers list
# The lambda function receives one number at a time

# x % 2 calculates the remainder after dividing x by 2.
# If the remainder is not 0, the number is odd

# x % 2 != 0 means: "Is the remainder different from 0?"
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)                                              # Print the numbers that passed the filter

#Output: [1, 3, 5, 7]