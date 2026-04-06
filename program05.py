#find count of particular file type in a directory
import os
path = input("enter file path:")
count = 0
for file in os.listdir(path):
    if file.endswith(".msi"):
        count+=1
print(".msi files found",count)
