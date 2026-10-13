#map fucntion returns the specified iterator with the specified function applied to each item

def myfunc(a):
  return len(a)

x = map(myfunc, ('apple', 'banana', 'cherry'))

print(x)

#convert the map into a list, for readability:
print(list(x))
#Output:
#<map object at 0x056D44F0>
#[5, 6, 6] 


#filter function used to exclude items in an iterable object

ages = [5, 12, 17, 18, 24, 32]

def myFunc(x):
  if x < 18:
    return False
  else:
    return True

adults = filter(myFunc, ages)

for x in adults:
  print(x)
#Output:
#18
#24
#32 

#reduce used to apply a function of two arguments cumulatively to the items of a sequence.
#in python 2 it was built-in, but in python 3 we need to import it

from functools import reduce
def add(a, b):
    return a + b
numbers = [1202334, -214253987.23, 21325365 ]
total = reduce(add, numbers)
print(total) 