#password check using api call by haveibeenpwned.com 
import hashlib, requests

password = input("Enter password: ")

# hash password
sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
print(sha1)
prefix = sha1[:5]
suffix = sha1[5:]

url = f"https://api.pwnedpasswords.com/range/{prefix}"
res = requests.get(url)

found = False
for line in res.text.splitlines():
    hash_suffix, count = line.split(":")
    if hash_suffix == suffix:
        print("Password leaked", count, "times!")
        found = True
        break

if not found:
    print("Password not found in breach database")
