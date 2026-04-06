#temp email detection using public disposable email list
import requests
#get domain from user input 
domain = input("Enter email: ").split("@")[-1]
# public disposable email list
url = "https://raw.githubusercontent.com/7c/fakefilter/main/txt/data.txt"

data = requests.get(url).text.splitlines()

if domain in data:
    print("Disposable email detected!")
else:
    print("Likely real email")
