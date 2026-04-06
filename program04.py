#intrnet connectivity check
import os 
import requests
try: 
 response =  requests.get("https://www.google.com")
 print(response)
except requests.exceptions.RequestException as e:
    print("network issue: ", e)
#final output
print(response.status_code)