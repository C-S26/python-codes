#password strength checker
password =  input("enter password: ")

if len(password) < 8:
   print("password isn't lengthy enough")
else:
    print("password is strong")