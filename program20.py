#open redirect checker
import requests

site = input("Site: ")
payload = "?redirect=https://evil.com"

r = requests.get(site+payload)

if "evil.com" in r.url:
    print("Open redirect possible")
else:
    print("No redirect detected")
