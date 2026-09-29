#random
import random

print(random.random()) 

#randint
import random

print(random.randint(3, 9)) 

#choice
import random

mylist = ["apple", "banana", "cherry"]

print(random.choice(mylist)) 

#shuffle
import random

mylist = ["apple", "banana", "cherry"]
random.shuffle(mylist)

print(mylist)