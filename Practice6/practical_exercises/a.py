import shutil
with open("file.txt", "a") as f:
    f.write("\nhuman")
shutil.move("file.txt", "m/file.txt" )