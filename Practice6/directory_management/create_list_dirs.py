import os
os.mkdir("myfolder")  # Creates one directory named myfolder


import os
os.makedirs("myfolder/subfolder")  # Creates myfolder and subfolder inside it


import os
print(os.listdir())  # Shows files and folders in the current directory


import os
os.chdir("myfolder")  # Moves into myfolder


import os
print(os.getcwd())  # Shows the path of the current directory


import os
os.rmdir("myfolder")  # Deletes myfolder if it is empty


from pathlib import Path

p = Path("/home/user") / "projects" / "demo.txt"
print(p.name)
print(p.parent)
print(p.suffix)
#Output:
#demo.txt
#/home/user/projects
#.txt

