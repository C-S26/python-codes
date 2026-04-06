#check internet connectivity and response 
import requests
response = requests.get("https://www.google.com")
print(response.headers)
