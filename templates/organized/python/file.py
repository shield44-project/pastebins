# class Employee: 
#     language = "Python" # This is a class attribute
#     salary = 1200000

#     def __init__(self, name, salary, language): # dunder method which is automatically called
#         self.name = name
#         self.salary = salary
#         self.language = language
#         print("I am creating an object")
 
 
#     def getInfo(self):
#         print(f"The language is {self.language}. The salary is {self.salary}")

#     @staticmethod
#     def greet():ject")
 
 
#     def getInfo(self):
#         print(f"The language is {self.language}. The salary is {self.salary}")

#     @staticmethod
#     def greet():
#         print("Good morning")


# harry = Employee("Harry", 1300000, "JavaScript") 
# # harry.name = "Harry"
# print(harry.name, harry.salary, harry.language)
# cipher = "KHOOR"

# for shift in range(26):
#     decrypted = ''
#     for c in cipher:
#         if c.isalpha():
#             decrypted += chr((ord(c) - shift - 65) % 26 + 65)
#         else:
#             decrypted += c
#     print(f"Shift {shift}: {decrypted}")

# print(ord('A'))
# MONSTERABCDFGHIJKLPQUVWXYZ
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
def vigenere_decrypt(ciphertext, key):
    decrypted = ''
    key = key.upper()
    for i, c in enumerate(ciphertext):
        if c.isalpha():
            shift = ord(key[i % len(key)]) - ord('A')
            decrypted += chr((ord(c) - shift - 65) % 26 + 65)
        else:
            decrypted += c
    return decrypted

print(vigenere_decrypt("WIMSICAL","KEY"))
