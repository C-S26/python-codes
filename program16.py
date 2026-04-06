#check for security headers in a website
import requests

url = input("Enter URL: ")

r = requests.get(url)
print(r.headers)
headers = ["X-Frame-Options", "Content-Security-Policy", "Strict-Transport-Security"]

for h in headers:
    if h in r.headers:
        print(h, "-> Present")
    else:
        print(h, "-> Missing (Potential Risk)")