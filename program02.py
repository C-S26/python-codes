#log file analysis
with open(r"C:\Users\pavan\Downloads\Android_2k.log", "r") as file:
  for line in file:
    if "1702" in line:
        print(line)
