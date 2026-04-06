#ceaser cipher alike encryption
def encrypt(text, shift):
    result = ""
    for ch in text:
        result += chr((ord(ch) + shift) % 256)
    return result

msg = input("Message: ")
enc = encrypt(msg, 4)

print("Encrypted:", enc)
print("Decrypted:", encrypt(enc, -4))
