


print("\n1 Ceaser Cipher\n2 Atbash Cipher\n3 Vigenère Cipher")

Ent=int(input("Enter the method of decoding cipher:"))
############                   ############
############   Ceaser Cypher   ############
############                   ############
if Ent==1:
    cipher = str(input("Enter your cipher:"))

    for shift in range(26):
        decrypted = ''
        for c in cipher:
            if c.isalpha():
                decrypted += chr((ord(c) - shift - 65) % 26 + 65)
            else:
                decrypted += c
        print(f"Shift {shift}: {decrypted}")




############                   ############
############   Atbash  Cypher  ############
############                   ############
elif Ent==2:
    text =str(input("Enter your cipher:"))
    decoded = ''
    for c in text:
        if c.isalpha():
            decoded += chr(155 - ord(c))  # 155 = ord('A') + ord('Z')
        else:
            decoded += c
    print(decoded)
else:
    print("Currently not working")


