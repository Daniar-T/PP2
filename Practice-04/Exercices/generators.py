#1. Create a generator that generates the squares of numbers up to some number `N`.

def squares_up_to(n):
    for number in range(n + 1):
        yield number ** 2


for square in squares_up_to(5):
    print(square)

#2. Write a program using generator to print the even numbers between 0 and `n` in comma separated form where `n` is input from console.

def even_numbers(n):
    for number in range(0, n + 1, 2):
        yield number


n = int(input("Enter n: "))

print(", ".join(str(number) for number in even_numbers(n)))

#3. Define a function with a generator which can iterate the numbers, which are divisible by 3 and 4, between a given range 0 and `n`.

def divisible_by_3_and_4(n):
    for number in range(n + 1):
        if number % 3 == 0 and number % 4 == 0:
            yield number


for number in divisible_by_3_and_4(50):
    print(number)

#4. Implement a generator called `squares` to yield the square of all numbers from (a) to (b). Test it with a "for" loop and print each of the yielded values.

def squares(a, b):
    for number in range(a, b + 1):
        yield number ** 2


for value in squares(2, 5):
    print(value)

#5. Implement a generator that returns all numbers from (n) down to 0.

def countdown(n):
    for number in range(n, -1, -1):
        yield number


for number in countdown(5):
    print(number)