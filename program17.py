#generate a secure password every time the program is run
import secrets
import string

chars = string.ascii_letters + string.digits + "@#$%&*'"
password = ''.join(secrets.choice(chars) for _ in range(20))

print("Secure password:", password)
