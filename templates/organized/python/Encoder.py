def caesar_encrypt(text, shift):
    result = ''
    for c in text.upper():
        if c.isalpha():
            result += chr((ord(c) - 65 + shift) % 26 + 65)
        else:
            result += c
    return result

def atbash_encrypt(text):
    result = ''
    for c in text.upper():
        if c.isalpha():
            result += chr(155 - ord(c))  # 155 = ord('A') + ord('Z')
        else:
            result += c
    return result

def vigenere_encrypt(text, key):
    result = ''
    key = key.upper()
    key_length = len(key)
    for i, c in enumerate(text.upper()):
        if c.isalpha():
            shift = ord(key[i % key_length]) - 65
            result += chr((ord(c) - 65 + shift) % 26 + 65)
        else:
            result += c
    return result

def main():
    print("=== Cipher Encoder ===")
    print("1. Caesar Cipher")
    print("2. Atbash Cipher")
    print("3. Vigenère Cipher")
    choice = input("Select cipher (1/2/3): ")

    message = input("Enter the message to encode: ")

    if choice == '1':
        shift = int(input("Enter the Caesar shift (0–25): "))
        print("Encoded:", caesar_encrypt(message, shift))

    elif choice == '2':
        print("Encoded:", atbash_encrypt(message))

    elif choice == '3':
        key = input("Enter the Vigenère key (e.g. 'KEY'): ")
        print("Encoded:", vigenere_encrypt(message, key))

    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()

else:
 print("idk")