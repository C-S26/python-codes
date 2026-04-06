#program 03
name = input("Name: ")
year = input("Birth year: ")

common = ["123", "1234", "@123", "13579", "admin", "qwerty"]
chars = "!@#$%^&*()"

for c in common:
    print(name + year + c)
    print(name + chars + year)
    print(name.capitalize() + c)
