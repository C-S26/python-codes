#password list check
password = "$pr1ng"

with open("seasons.txt", "r") as file:
    for line in file:
        guess = line.strip()

        if guess == password:
            print("Password found:", guess)
            break