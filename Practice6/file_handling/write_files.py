#"w" - Write - will overwrite any existing content
with open("demofile.txt", "w") as f:
  f.write("Woops! I have deleted the content!")


#open and read the file after the overwriting:

with open("demofile.txt") as f:
  print(f.read())
#Output:
#Woops! I have deleted the content! 


#"a" - Append - will append to the end of the file

with open("demofile.txt", "a") as f:
  f.write("Now the file has more content!")


#open and read the file after the appending:

with open("demofile.txt") as f:
  print(f.read())
#Output:
#Hello! Welcome to demofile.txt
#This file is for testing purposes.
#Good Luck!Now the file has more content!   

  
#"x" - Create - will create a file, returns an error if the file exists

#This will create a new file:
f = open("myfile.txt", "x")
#If the file already exist, an error will be raised.
