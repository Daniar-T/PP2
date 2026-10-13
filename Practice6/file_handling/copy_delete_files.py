#To delete a file import the OS module, and run its os.remove() function:
import os
os.remove("demofile.txt") 


#To delete an entire folder, use the os.rmdir() method:
import os
os.rmdir("myfolder") 


#to copy the file import shutil and run its shutil.copy function:
import shutil

# Copy a file
shutil.copy("file.txt")