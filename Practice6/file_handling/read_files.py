#readline()
#Read one line of the file:

f = open("demofile.txt")
print(f.readline())

#to close the file use close() statement 
f.close() 
#Output: Hello! Welcome to demofile.txt 


#readlines
#reads a file and returns all its lines as a list, where each line is a separate item.

f = open("demofile.txt")
print(f.readlines())
f.close
#Output:
#['Hello! Welcome to demofile.txt\n', 'This file is for testing purposes.\n', 'Good Luck!']

#if other location specify the file path

f = open("D:\\myfiles\welcome.txt")
print(f.read()) 
#Output: 
#Welcome to this text file!
#This file is located in a folder named "myfiles", on the D drive.
#Good Luck! 


#reads only part of file
#with statement takes care of closing file

with open("demofile.txt") as f:
  print(f.read(5)) 
#Output: Hello


#for loop

with open("demofile.txt") as f:
  for x in f:
    print(x)
#Output: Hello! 
#Welcome to demofile.txt
#
#This file is for testing purposes.
#
#Good Luck! 