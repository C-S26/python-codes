import hashlib

# load hashes
users = {}
with open("users.txt") as f:
    for line in f:
        user, h = line.strip().split(":")
        users[h] = user

# try cracking
with open("wordlist.txt") as f:
    for word in f:
        word = word.strip()
        h = hashlib.sha1(word.encode()).hexdigest()

        if h in users:
            print(users[h], "password is:", word)


