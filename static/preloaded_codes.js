// Auto-generated file with pre-loaded code files
// Generated from stored_codes/ directory

const PRELOADED_CODES = [
  {
    "id": "python_0",
    "language": "python",
    "title": "Encoder",
    "description": "Migrated from templates/code_samples/python/Encoder.py",
    "filename": "Encoder.py",
    "code": "def caesar_encrypt(text, shift):\n    result = ''\n    for c in text.upper():\n        if c.isalpha():\n            result += chr((ord(c) - 65 + shift) % 26 + 65)\n        else:\n            result += c\n    return result\n\ndef atbash_encrypt(text):\n    result = ''\n    for c in text.upper():\n        if c.isalpha():\n            result += chr(155 - ord(c))  # 155 = ord('A') + ord('Z')\n        else:\n            result += c\n    return result\n\ndef vigenere_encrypt(text, key):\n    result = ''\n    key = key.upper()\n    key_length = len(key)\n    for i, c in enumerate(text.upper()):\n        if c.isalpha():\n            shift = ord(key[i % key_length]) - 65\n            result += chr((ord(c) - 65 + shift) % 26 + 65)\n        else:\n            result += c\n    return result\n\ndef main():\n    print(\"=== Cipher Encoder ===\")\n    print(\"1. Caesar Cipher\")\n    print(\"2. Atbash Cipher\")\n    print(\"3. Vigenère Cipher\")\n    choice = input(\"Select cipher (1/2/3): \")\n\n    message = input(\"Enter the message to encode: \")\n\n    if choice == '1':\n        shift = int(input(\"Enter the Caesar shift (0–25): \"))\n        print(\"Encoded:\", caesar_encrypt(message, shift))\n\n    elif choice == '2':\n        print(\"Encoded:\", atbash_encrypt(message))\n\n    elif choice == '3':\n        key = input(\"Enter the Vigenère key (e.g. 'KEY'): \")\n        print(\"Encoded:\", vigenere_encrypt(message, key))\n\n    else:\n        print(\"Invalid choice. Exiting.\")\n\nif __name__ == \"__main__\":\n    main()\n\nelse:\n print(\"idk\")",
    "created": "2025-11-09T13:25:08.354785"
  },
  {
    "id": "python_1",
    "language": "python",
    "title": "Add",
    "description": "Migrated from templates/code_samples/python/add.py",
    "filename": "add.py",
    "code": "number1=int(input(\"Enter number1:\"))\nnumber2=int(input(\"Enter number2:\"))\nsum=number1+number2\nprint(f\"Sum of the numbers {number1} and {number2} is {sum}\")\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_2",
    "language": "python",
    "title": "Advancedpython",
    "description": "Migrated from templates/code_samples/python/advancedpython.py",
    "filename": "advancedpython.py",
    "code": "####WALRUS\n# if (n := len([1, 2, 3, 4, 5])) > 3:\n#         print(f\"List is too long ({n} elements, expected <= 3)\")\n\n# age: int=233\n# def whatisthis(name: str) -> str:\n#     return f\"Hello {name}\"\n# print(whatisthis(\"Yashas\"))\n# def sum(a: int,b: int) -> int:\n#     return a+b\n# print(sum(3,5))\nfrom typing import List, Tuple, Dict, Union\n# List of integers\nnumbers: List[int] = [1, 2, 3, 4, 5]\n# Tuple of a string and an integer\nperson: Tuple[str, int] = (\"Alice\", 30)\n# Dictionary with string keys and integer values\nscores: Dict[str, int] = {\"Alice\": 90, \"Bob\": 85}\n# Union type for variables that can hold multiple types\nidentifier: Union[int, str] = \"ID123\"\nidentifier = 12345 # Also valid\n\n\n# #####MATCH CASE#########\n# def http_status(status):\n#     match status:\n#         case 200:\n#             return \"OK\"\n#         case 404:\n#             return \"Not Found\"\n#         case 500:\n#             return \"Internal Server Error\"\n#         case _:\n#             return \"Unknown status\"\n# print(http_status(200))\n# dict1={\"a\":1,\"b\":2}\n# dict2={\"c\":3,\"d\":4}\n# merged= dict1 | dict2\n# print(merged)\n# with (\n# open('file1.txt') as f1,\n# open('file2.txt') as f2\n# ):\n# Process files\n# try:\n#     a=int(input(\"Enter the number:\"))\n# except Exception as e:\n#       print(e)\n\n# L={1,2,3,4,5,6,7,8}\n# for i,item in enumerate(L):\n#     if i==2 or i==4 or i==6:\n#         print(item)\n# def sq(n):\n#     return n*n\n# sq=lambda x:x*x \n# bq= lambda a,b,c:a+b+c\n# print(sq(2))\n# print(bq(3,4,5))\na=[\"a\",\"pp\",\"le\"]\njointhem=\"\".join(a) # \"put anything here they will join the list elements\"\nprint(jointhem)\nl=\"{1} is a good {0}\".format(\"Harry\",\"boy\")\nprint(l)\nL=[1,2,3,4,5,6,7,8]\nsw=lambda x:x*x*x\nswlist=map(sw,L)\nprint(list(swlist))\n#filter\ndef odd(n):\n    if(n%2!=0):\n        return True\n    return False\nl=filter(odd,L)\nprint(list(l))\n# reduce\ndef sum(a,b):\n    return a+b\nfrom functools import reduce\nmul=lambda x,y:x*y\nprint(reduce(mul,L))\nprint(reduce(sum,L))\n\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_3",
    "language": "python",
    "title": "Arm",
    "description": "Migrated from templates/code_samples/python/arm.py",
    "filename": "arm.py",
    "code": "#389=3^3+8^3+9^3 is called armstrong number(if)\n#xyz=x^n+y^n+z^n armstrong number of order n\n\"\"\"\n9981%10=1\n998%10=8\n99%10=9\n9%10=9\"\"\"\nn=153\nsum=0\ncopy=n\norder=len(str(n))\nwhile(n>0):\n\tdigit=n%10\n\tsum+=digit**order\n\tn=n//10 # 8891 ko 889 so floor division whener number >0 it works\nif sum==copy:\n\tprint(\"Armstrong number of order \",order)\nelse:\n\tprint(\"Not a armstrong number\")\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_4",
    "language": "python",
    "title": "Body",
    "description": "Migrated from templates/code_samples/python/body.py",
    "filename": "body.py",
    "code": "weight=float(input(\"Enter your weight in kg:\"))\nheight=float(input(\"Enter your length in metre:\"))\nbmi=weight/height**2\n\nprint(f\"Your BMI is \",bmi)\n\nif bmi<18.5:\n\tprint(\"You are underweight\")\nelif bmi>=18.5 and bmi<=24.9:\n\tprint(\"You are normal weight\")\nelif bmi>=25 and bmi<=29.9:\n\tprint(\"You're overweight\")\nelse:\n\tprint(\"You are obese\")\n\n\n\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_5",
    "language": "python",
    "title": "Cal",
    "description": "Migrated from templates/code_samples/python/cal.py",
    "filename": "cal.py",
    "code": "import calendar\n\nYEAR=int(input(\"Y:\"))\nMON=int(input(\"M:\"))\nprint(calendar.month(YEAR,MON))\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_6",
    "language": "python",
    "title": "Circle",
    "description": "Migrated from templates/code_samples/python/circle.py",
    "filename": "circle.py",
    "code": "import math\n\nrad=int(input(\"Enter the radius of circle:\"))\narea=math.pi*pow(rad,2)\nprint(\"Area of circle of radius {0} : {1}\".format(rad,area))\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_7",
    "language": "python",
    "title": "Crypt4digit",
    "description": "Migrated from templates/code_samples/python/crypt4digit.py",
    "filename": "crypt4digit.py",
    "code": "import secrets\npin = ''.join(str(secrets.randbelow(10)) for _ in range(4))\nprint(pin)\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_8",
    "language": "python",
    "title": "Decoder",
    "description": "Migrated from templates/code_samples/python/decoder.py",
    "filename": "decoder.py",
    "code": "\n\n\nprint(\"\\n1 Ceaser Cipher\\n2 Atbash Cipher\\n3 Vigenère Cipher\")\n\nEnt=int(input(\"Enter the method of decoding cipher:\"))\n############                   ############\n############   Ceaser Cypher   ############\n############                   ############\nif Ent==1:\n    cipher = str(input(\"Enter your cipher:\"))\n\n    for shift in range(26):\n        decrypted = ''\n        for c in cipher:\n            if c.isalpha():\n                decrypted += chr((ord(c) - shift - 65) % 26 + 65)\n            else:\n                decrypted += c\n        print(f\"Shift {shift}: {decrypted}\")\n\n\n\n\n############                   ############\n############   Atbash  Cypher  ############\n############                   ############\nelif Ent==2:\n    text =str(input(\"Enter your cipher:\"))\n    decoded = ''\n    for c in text:\n        if c.isalpha():\n            decoded += chr(155 - ord(c))  # 155 = ord('A') + ord('Z')\n        else:\n            decoded += c\n    print(decoded)\nelse:\n    print(\"Currently not working\")\n\n\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_9",
    "language": "python",
    "title": "Eigen",
    "description": "Migrated from templates/code_samples/python/eigen.py",
    "filename": "eigen.py",
    "code": "import numpy as np\n\nmatrix=np.array([x,y,z],[a,b,c],[d,e,f])\nx=int(input(\"Enter value for Mat(1,1): \"))\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_10",
    "language": "python",
    "title": "Factorial",
    "description": "Migrated from templates/code_samples/python/factorial.py",
    "filename": "factorial.py",
    "code": "n=int(input(\"Enter a number:\"))\nproduct=1\nfor i in range(1,n+1):\n    product=product*i\n\nprint(f\"Factorial of {n} is {product}:\")",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_11",
    "language": "python",
    "title": "Factrecursion",
    "description": "Migrated from templates/code_samples/python/factrecursion.py",
    "filename": "factrecursion.py",
    "code": "def facto(n):\n    if(n==0 or n==1):\n        return 1\n    return n*facto(n-1)\nn=int(input(\"Enter a number:\"))\nprint(f\"The factorial of this number is : {facto(n)}\")\n\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_12",
    "language": "python",
    "title": "File",
    "description": "Migrated from templates/code_samples/python/file.py",
    "filename": "file.py",
    "code": "# class Employee: \n#     language = \"Python\" # This is a class attribute\n#     salary = 1200000\n\n#     def __init__(self, name, salary, language): # dunder method which is automatically called\n#         self.name = name\n#         self.salary = salary\n#         self.language = language\n#         print(\"I am creating an object\")\n \n \n#     def getInfo(self):\n#         print(f\"The language is {self.language}. The salary is {self.salary}\")\n\n#     @staticmethod\n#     def greet():ject\")\n \n \n#     def getInfo(self):\n#         print(f\"The language is {self.language}. The salary is {self.salary}\")\n\n#     @staticmethod\n#     def greet():\n#         print(\"Good morning\")\n\n\n# harry = Employee(\"Harry\", 1300000, \"JavaScript\") \n# # harry.name = \"Harry\"\n# print(harry.name, harry.salary, harry.language)\n# cipher = \"KHOOR\"\n\n# for shift in range(26):\n#     decrypted = ''\n#     for c in cipher:\n#         if c.isalpha():\n#             decrypted += chr((ord(c) - shift - 65) % 26 + 65)\n#         else:\n#             decrypted += c\n#     print(f\"Shift {shift}: {decrypted}\")\n\n# print(ord('A'))\n# MONSTERABCDFGHIJKLPQUVWXYZ\n# ABCDEFGHIJKLMNOPQRSTUVWXYZ\n# ABCDEFGHIJKLMNOPQRSTUVWXYZ\n# ABCDEFGHIJKLMNOPQRSTUVWXYZ\n# ABCDEFGHIJKLMNOPQRSTUVWXYZ\n# ABCDEFGHIJKLMNOPQRSTUVWXYZ\n# ABCDEFGHIJKLMNOPQRSTUVWXYZ\n# ABCDEFGHIJKLMNOPQRSTUVWXYZ\n# ABCDEFGHIJKLMNOPQRSTUVWXYZ\n# ABCDEFGHIJKLMNOPQRSTUVWXYZ\n# ABCDEFGHIJKLMNOPQRSTUVWXYZ\ndef vigenere_decrypt(ciphertext, key):\n    decrypted = ''\n    key = key.upper()\n    for i, c in enumerate(ciphertext):\n        if c.isalpha():\n            shift = ord(key[i % len(key)]) - ord('A')\n            decrypted += chr((ord(c) - shift - 65) % 26 + 65)\n        else:\n            decrypted += c\n    return decrypted\n\nprint(vigenere_decrypt(\"WIMSICAL\",\"KEY\"))\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_13",
    "language": "python",
    "title": "Fn",
    "description": "Migrated from templates/code_samples/python/fn.py",
    "filename": "fn.py",
    "code": "def hel():\n    user=input(\"Enter your user id:\")\n    print(f\"Hello {user}\")\n\nhel()",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_14",
    "language": "python",
    "title": "Fnarg",
    "description": "Migrated from templates/code_samples/python/fnarg.py",
    "filename": "fnarg.py",
    "code": "def tat(unknown,ending=\"Let be me let me see tryna shut me down \"):\n    product=\"Let me do some \" + unknown\n    print(product)\n    print(ending)\n    return \"bye\"\n \nu=tat(\"magic\",\"Tryna do something new\")\ntat(\"thing\")\nprint(u)",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_15",
    "language": "python",
    "title": "Gratio",
    "description": "Migrated from templates/code_samples/python/gratio.py",
    "filename": "gratio.py",
    "code": "n=int(input(\"Enter a number:\"))\nfiblist=[0,1]\nfor i in range(0,n):\n\tfiblist.append(fiblist[i]+fiblist[i+1])\nprint(fiblist)\ngratio=[fiblist[i]/float(fiblist[i-1]) for i in range(2,len(fiblist)) ]\nprint(gratio)\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_16",
    "language": "python",
    "title": "Guess",
    "description": "Migrated from templates/code_samples/python/guess.py",
    "filename": "guess.py",
    "code": "import random\n\nno = random.randint(1, 100)\ntries = 0\n\nguess = int(input(\"Enter your guess: \"))\ntries += 1\n\nwhile guess != no:\n    if guess > no:\n        print(\"Your guess is higher than the number.\")\n    else:\n        print(\"Your guess is lower than the number.\")\n    guess = int(input(\"Try again: \"))\n    tries += 1\n\nprint(f\"You guessed it correct! The number is {no}.\")\nprint(f\"It took you {tries} tries.\")\n\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_17",
    "language": "python",
    "title": "Hcf",
    "description": "Migrated from templates/code_samples/python/hcf.py",
    "filename": "hcf.py",
    "code": "num1=int(input(\"Number1: \"))\nnum2=int(input(\"Number2: \"))\n# if num1>num2 :\n# \tmn=num1\n# else:\n# \tmn=num2\n# for i in range(1,mn+1):\n# \tif num1%i==0 and num2%i==0:\n# \t\thcf=i\n# print(hcf)\n\nif num1>num2:\n    mn=num1\nelse:\n    mn=num2\nfor i in range(1,mn+1):\n    if num1%i==0 and num2%i==0:\n        hcf=i\nprint(hcf)",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_18",
    "language": "python",
    "title": "Hello",
    "description": "Migrated from templates/code_samples/python/hello.py",
    "filename": "hello.py",
    "code": "print(\"Hello World!\")\n\nprint(\"Hello this is a python file and it runs print function. /n Python is a very useful programming language./n Python is easy to use and also has many inbuilt functions\")\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_19",
    "language": "python",
    "title": "Lcm",
    "description": "Migrated from templates/code_samples/python/lcm.py",
    "filename": "lcm.py",
    "code": "a=int(input(\"Number1: \"))\nb=int(input(\"Number2: \"))\n# maxNum=max(a,b)\n# while(True):\n# \tif(maxNum%a==0 and maxNum%b==0):\n# \t\tbreak\n# \tmaxNum=maxNum+1\n\n# print(maxNum)\n\nlcm=max(a,b)\nwhile(True):\n    if (lcm%a==0 and lcm%b==0):\n        break\n    lcm=lcm+1\nprint(lcm)\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_20",
    "language": "python",
    "title": "Matrics",
    "description": "Migrated from templates/code_samples/python/matrics.py",
    "filename": "matrics.py",
    "code": "A=[[1,2,5],[3,4,7],[5,6,9]]\nB=[[1,3],[3,4],[7,6]]\nC=[[0,0],[0,0],[0,0]]\nfor i in range(0,len(C)):\n\tfor j in range(1,len(C[0])):\n\t\tfor k in range(1,len(B)):\n\t\t\tC[i][j]+=A[i][k] * B[k][j]\nfor row in C:\n\tprint(row)\n\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_21",
    "language": "python",
    "title": "Maxprime",
    "description": "Migrated from templates/code_samples/python/maxprime.py",
    "filename": "maxprime.py",
    "code": "n=int(input(\"Enter a number:\"))\nmaxprim=-1\n\nwhile n%2==0:\n\tmaxprim=n\n\tn=n/2\n\nfor i in range(3,int(n**(0.5))+1,2):\n\twhile n%i==0:\n\t\tmaxprim=i\n\t\tn=n/i\n\tif n>2:\t\n\t\tmaxprim=n\nprint(maxprim)\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_22",
    "language": "python",
    "title": "Numpy C1",
    "description": "Migrated from templates/code_samples/python/numpy_c1.py",
    "filename": "numpy_c1.py",
    "code": "import numpy as np\n\nprint(np.__version__) # __ is called dunder\narray=np.array([1,2,3])\nprint(np.ndim)\nprint(array)\nprint(array*2)\nprint(array[0:1:2])\nprint(np.sqrt(array))\nprint(np.floor(array))\nradii=4\nnp.pi*radii**2",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_23",
    "language": "python",
    "title": "P1",
    "description": "Migrated from templates/code_samples/python/p1.py",
    "filename": "p1.py",
    "code": "a=int(input(\"a is :\"))\nb=int(input(\"b is :\"))\nprint(\"Remainder of a/b is :\", a % b)\nprint(type(a))\nprint(\"a is greater than b\", a>b)\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_24",
    "language": "python",
    "title": "P10",
    "description": "Migrated from templates/code_samples/python/p10.py",
    "filename": "p10.py",
    "code": "l=[\"Harry\",\"Sam\",\"Petere\",\"Samuel\",\"Sasaki\",\"Saitama\"]\nfor i in l:\n    if(i.startswith(\"S\")):\n       print(f\"Hello {i}\")",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_25",
    "language": "python",
    "title": "P12",
    "description": "Migrated from templates/code_samples/python/p12.py",
    "filename": "p12.py",
    "code": "# n=int(input(\"Enter the number:\"))\n# v=0\n# for i in range(1,n+1):\n#     v+=i\n\n# print(v)\n\n# n=int(input(\"Enter the number:\"))\n# p=1\n# for m in range(1,n+1):\n#     p=p*m\n# print(p)\n# n=int(input(\"Enter the number:\"))\n# v=0\n# for i in range(1,n+1):\n#     v+=i/2\n# print(v)\n# n=int(input(\"Enter the number:\"))\n# for i in range(2,n):\n#    if(n%i==0):\n#        print(\"The number is not prime\")\n#        break\n# else:\n#        print(\"The number is prime\")\n# n=int(input(\"Enter the number:\"))\n# i=1\n# for i in range(1,n+1):\n#     print(\" \"*(n-1), end=\"\")\n#     print(\"\")\n#     print(\"*\"*(i), end=\"\")\n# print(\"\")\n\n# n = int(input(\"Enter the number: \"))\n# for i in range(1, n+1): \n#     if(i==1 or i==n):\n#         print(\"*\"* n, end=\"\")\n#     else:\n#         print(\"*\", end=\"\")\n#         print(\" \"* (n-2), end=\"\")\n#         print(\"*\", end=\"\")\n#     print(\"\")\n# n = int(input(\"Enter the number: \"))\n# for i in range(1,11):\n#     print(f\"{n}X{11-i}={n*(11-i)}\")\n# n=int(input(\"Enter the number:\"))\n# for i in range(1,n+1):\n#     print(\" \"*(n-i), end=\"\")\n#     print(\"*\"*(2*i-1), end=\"\")\n#     print(\"\")\n# a=int(input(\"Enter a number:\"))\n# b=int(input(\"Enter a number:\"))\n# c=int(input(\"Enter a number:\"))\n# if(a>b and a>c):\n#         print(f\"{a} is the greatest number\")\n# elif(b>a and b>c):\n#         print(f\"{b} is the greatest number\")\n# else:\n#         print(f\"{c} is the greatest number\")\n# def use(a,b,c):\n#     if(a>b and a>c):\n#         return a\n#     if(b>a and b>c):\n#         return b\n#     if(c>a and c>b):\n#         return c\n# a=int(input(\"Enter a number:\"))\n# b=int(input(\"Enter a number:\"))\n# c=int(input(\"Enter a number:\"))\n# print(use(a,b,c))\n# c=int(input(\"Enter a number:\"))\n# def ctof():\n#     return 9/5*(c)+32\n# print(f\"{round(ctof(),4)}°F\")\n# f=int(input(\"Enter a number:\"))\n# def ftoc():\n#     return (5*(f-32))/9\n# print(f\"{round(ftoc(),2)}°C\")\n# def f_to_c(f):\n#     return 5*(f-32)/9\n\n# f = int(input(\"Enter temperature in F: \"))\n# c = f_to_c(f)\n# print(f\"{round(c, 2)}°C\")\n# i=   int(input(\"Enter a number:\"))       \n# def fa(n):\n#     if(n==1 or n==0):\n#         return 1\n#     else:\n#             return n*fa(n-1)\n# print(fa(i)) \n# number=int(input(\"Enter a number:\"))\n# def sum_of_n_natural_numbers(n):\n#        if(n==1): \n# def pattern(n):\n#     if(n==0):\n#         return\n#     print(\"*\" * n)\n#     pattern(n-1)\n\n\n# pattern(3)\n# inch=int(input(\"Enter the number:\"))\n# def intocm(inch):\n#     return inch*2.54\n# print(intocm(4))\n# def pattern(n):\n#      if(n==0):\n#           return\n#      else:\n#           print(\"*\"*n)\n#           pattern(n-1)\n\n# pattern(3)\n# def rem(l,word):\n#     n=[]\n#     for item in l:\n#         if not(item==word):\n#             n.append(item.strip(word))\n#         return n\n# l = [\"Harry\", \"Rohan\", \"Shubham\", \"an\"]\n# print(rem(l, \"an\"))\n# def mult(n):\n#     for i in range(1,11):\n#         print(f\"{n}X{i}={n*i}\")\n     \n# mult(3)",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_26",
    "language": "python",
    "title": "P2",
    "description": "Migrated from templates/code_samples/python/p2.py",
    "filename": "p2.py",
    "code": "letter = '''Dear <|Name|>, \nYou are selected! \n<|Date|> '''\n\nprint(letter.replace(\"<|Name|>\", \"user\").replace(\"<|Date|\", \"24 September 2050\"))\n\nname=\"what is  this  lol  \"\nprint(name.replace(\"  \", \" \"))",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_27",
    "language": "python",
    "title": "P3",
    "description": "Migrated from templates/code_samples/python/p3.py",
    "filename": "p3.py",
    "code": "d=(23,234,256,276)\n#a,b,c,e=d\n#print(a+b+c+e)\nprint(sum(d))\na=(3,0,0,00000,0,0,23,2,2)\nz=a.count(0)\nprint(z)",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_28",
    "language": "python",
    "title": "P4",
    "description": "Migrated from templates/code_samples/python/p4.py",
    "filename": "p4.py",
    "code": "h={\n\"こんにちは (Konnichiwa)\": \"Hello Good afternooon\",\n\"ありがとう (Arigatou)\":  \"Thank you\",\n\"おはよう (Ohayou)\t\": \"Good morning\",\n\"こんばんは (Konbanwa)\": \"Good evening\",\n\"おやすみ (Oyasumi)\":\t\"Good night\",\n\"愛 (Ai)\":\t\"Love\",\n\"平和 (Heiwa)\":\t\"Peace\",\n\"友達 (Tomodachi)\":\t\"Friend\",\n\"時間 (Jikan)\":\t\"Time\",\n\"空 (Sora)\":\t\"Sky\",\n\"水 (Mizu)\":\t\"Water\",\n\"火 (Hi)\":\t\"Fire\",\n\"夢 (Yume)\":\t\"Dream\",\n\"希望 (Kibou)\":\t\"Hope\",\n\"幸せ (Shiawase)\":\t\"Happiness\"\n}\n\nn=input(\"Enter the meaning of word u want:\")\nprint(h[n])",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_29",
    "language": "python",
    "title": "P5",
    "description": "Migrated from templates/code_samples/python/p5.py",
    "filename": "p5.py",
    "code": "s=set()\nn=input(\"Enter number here:\")\ns.add(int(n))\nn=input(\"Enter number here:\")\ns.add(int(n))\nn=input(\"Enter number here:\")\ns.add(int(n))\nn=input(\"Enter number here:\")\ns.add(int(n))\nn=input(\"Enter number here:\")\ns.add(int(n))\nn=input(\"Enter number here:\")\ns.add(int(n))\n\nprint(s)\n\n\n\n\n\n\n\n\n\n\n\n\n\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_30",
    "language": "python",
    "title": "P6",
    "description": "Migrated from templates/code_samples/python/p6.py",
    "filename": "p6.py",
    "code": "d={}\nn=input(\"Raam enter your fav language:\")\ng=input(\"Shaam enter your fav language:\")\nf=input(\"Sharan enter your fav language:\")\nk=input(\"Sam enter your fav language:\")\nd.update({\"Raam\":n,\"Shaam\":g,\"Sharan\":f,\"Sam\":k})\nprint(d)",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_31",
    "language": "python",
    "title": "P8",
    "description": "Migrated from templates/code_samples/python/p8.py",
    "filename": "p8.py",
    "code": "marks1 = int(input(\"Enter Marks 1: \"))\nmarks2 = int(input(\"Enter Marks 2: \"))\nmarks3 = int(input(\"Enter Marks 3: \"))\n\n# Check for total percentage\ntotal_percentage = (100*(marks1 + marks2 + marks3))/300\n\nif(total_percentage>=40 and marks1>=33 and marks2>=33 and marks3>=33):\n    print(\"You are passed:\", total_percentage)\n\nelse:\n    print(\"You failed, try again next year:\", total_percentage)",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_32",
    "language": "python",
    "title": "Para",
    "description": "Migrated from templates/code_samples/python/para.py",
    "filename": "para.py",
    "code": "str=\"New Delhi is capital of India,Bengaluru is capital of karnataka\"\nlist_str=str.split()\ncountwords=len(list_str)\nprint(\"The paragraph from the user has {0} words\".format(countwords))\n#frequency of words\n\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_33",
    "language": "python",
    "title": "Pass",
    "description": "Migrated from templates/code_samples/python/pass.py",
    "filename": "pass.py",
    "code": "for i in range(1000):\n    pass\ni=0\nwhile(i<45):\n    print(i)\n    i+=1",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_34",
    "language": "python",
    "title": "Perfect",
    "description": "Migrated from templates/code_samples/python/perfect.py",
    "filename": "perfect.py",
    "code": "num=int(input(\"Enter a number:\"))\n\nsum=0\n\nfor i in range(1,num):\n\tif num%i==0:\n\t\tsum=sum+i\nif sum==num:\n\tprint(f\"{sum} is a perfect number\")\nelse:\n\tprint(\"Not a perfect number\")\n",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_35",
    "language": "python",
    "title": "Plot",
    "description": "Migrated from templates/code_samples/python/plot.py",
    "filename": "plot.py",
    "code": "import matplotlib.pyplot as plt\nimport numpy as np      \nimport pyaudio as pa\ndef plot_waveform(waveform, sample_rate=44100):\n    \"\"\"\n    Plots the waveform of an audio signal.\n    \n    Parameters:\n    waveform (numpy.ndarray): The audio signal to plot.\n    sample_rate (int): The sample rate of the audio signal.\n    \"\"\"\n    plt.figure(figsize=(12, 4))\n    time = np.arange(len(waveform)) / sample_rate\n    plt.plot(time, waveform)\n    plt.title('Waveform')\n    plt.xlabel('Time [s]')\n    plt.ylabel('Amplitude')\n    plt.grid()\n    plt.show()\n    plt.show(block=False)\n    UnicodeTranslateError\n    ",
    "created": "2025-11-09T13:25:08.355785"
  },
  {
    "id": "python_36",
    "language": "python",
    "title": "Priime",
    "description": "Migrated from templates/code_samples/python/priime.py",
    "filename": "priime.py",
    "code": "n=int(input(\"Enter a number:\"))\n\nfor i in range(1,n):\n    if(n%i) ==0:\n        print(\"The number is not prime\")\n    break\nelse:\n    print(\"The number is prime\")\n\n    print(\"End of program\")",
    "created": "2025-11-09T13:25:08.356785"
  },
  {
    "id": "python_37",
    "language": "python",
    "title": "Prob1",
    "description": "Migrated from templates/code_samples/python/prob1.py",
    "filename": "prob1.py",
    "code": "ok=input(\"Enter your name:\")\nprint(f\"Good afternoon {ok}\")",
    "created": "2025-11-09T13:25:08.356785"
  },
  {
    "id": "python_38",
    "language": "python",
    "title": "Problem1",
    "description": "Migrated from templates/code_samples/python/problem1.py",
    "filename": "problem1.py",
    "code": "print(''' a b c what is this wiskqosk cmdfsavdx zANuegwBFDSWQ2197654    51\n      SEDRGHJYFDVSCZAAsdfg\n      rwefdgtbygfr3e2wdrfvgd''')",
    "created": "2025-11-09T13:25:08.356785"
  },
  {
    "id": "python_39",
    "language": "python",
    "title": "Revers",
    "description": "Migrated from templates/code_samples/python/revers.py",
    "filename": "revers.py",
    "code": "n=1245\nrev_n=0\nwhile n!=0:\n\tdigit=n%10\n\trev_n=digit*10+rev_n\n\tn//=10\nprint(rev_n)\n",
    "created": "2025-11-09T13:25:08.356785"
  },
  {
    "id": "python_40",
    "language": "python",
    "title": "Rough",
    "description": "Migrated from templates/code_samples/python/rough.py",
    "filename": "rough.py",
    "code": "# self.n=n\n#     def root(self):\n#         print(f\"The root is {self.n**(1/2)}\")\n#     @staticmethod\n#     def greet():\n#         print(\"Hello user\")\n# u=cal(calculator)\n# u.greet()\n# u.root()\n# class o:\n#     a=1\n# print(o.a)\n# o.a=32\n# print(o.a)",
    "created": "2025-11-09T13:25:08.356785"
  },
  {
    "id": "python_41",
    "language": "python",
    "title": "Seq",
    "description": "Migrated from templates/code_samples/python/seq.py",
    "filename": "seq.py",
    "code": "sequence=[4,None,6,9,0,None,None,65,90]\nprint(\"Original Sequence:\",sequence)\nfilled_seq=[]\nfor num in sequence:\n\tif num is None:\n\t\tfilled_seq.append(0)\n\telse:\n\t\tfilled_seq.append(num)\nprint(\"Sequence after replacing None with 0:\", filled_seq)\nprint(\"Removed second index in sequence:\",sequence.pop(2),sequence)\nprint(\"Added element 45 to the sequence:\",sequence.append(45),sequence)\nprint(\"Modified Sequence:\",sequence)\n\n",
    "created": "2025-11-09T13:25:08.356785"
  },
  {
    "id": "python_42",
    "language": "python",
    "title": "Seque",
    "description": "Migrated from templates/code_samples/python/seque.py",
    "filename": "seque.py",
    "code": "sequence = [4, None, 6, 9, 0, None, None, 65, 90]\n\nprint(\"Original Sequence:\", sequence)\n\n# Fill missing values (replace None with 0)\nfor i in range(len(sequence)):\n    if sequence[i] is None:\n        sequence[i] = 0\nprint(\"After Filling Missing Values:\", sequence)\n\n# Remove a number (remove element at index 2)\nremoved = sequence.pop(2)\nprint(\"After Removing Element at index 2 (removed:\", removed, \"):\", sequence)\n\n# Add a new number (e.g., 45)\nsequence.append(45)\nprint(\"After Adding Element 45:\", sequence)\n\nprint(\"Modified Sequence:\", sequence)\n\n",
    "created": "2025-11-09T13:25:08.356785"
  },
  {
    "id": "python_43",
    "language": "python",
    "title": "Set Meth",
    "description": "Migrated from templates/code_samples/python/set_meth.py",
    "filename": "set_meth.py",
    "code": "l={1,2,\"s\",\"d\",123223}\n#l.add(1029387)\n#print(l,type(l))\nl.remove(1)\nl.add(\"me\")\nl.sort()\nprint(l)",
    "created": "2025-11-09T13:25:08.356785"
  },
  {
    "id": "python_44",
    "language": "python",
    "title": "Sets",
    "description": "Migrated from templates/code_samples/python/sets.py",
    "filename": "sets.py",
    "code": "l={0,1.2,2,34,134,2343,1,1,1,1,1,1,1,1,1}\n#e=set()\nprint(l)",
    "created": "2025-11-09T13:25:08.356785"
  },
  {
    "id": "python_45",
    "language": "python",
    "title": "Sine Plot",
    "description": "Migrated from templates/code_samples/python/sine_plot.py",
    "filename": "sine_plot.py",
    "code": "import matplotlib.pyplot as plt\nimport numpy as np\n\n# Create data points from 0 to 2π (about 6.28)\nx = np.linspace(0, 2 * np.pi, 100)  # 100 points\ny = np.sin(x)  # Sine of each x\n\n# Plot\nplt.plot(x, y, label=\"sin(x)\", color=\"blue\", linewidth=2)\n\n# Labels and title\nplt.xlabel(\"x (radians)\")\nplt.ylabel(\"sin(x)\")\nplt.title(\"Sine Wave\")\n\n# Add grid and legend\nplt.grid(True)\nplt.legend()\n\n# Show\nplt.show()\n",
    "created": "2025-11-09T13:25:08.356785"
  },
  {
    "id": "python_46",
    "language": "python",
    "title": "Stri",
    "description": "Migrated from templates/code_samples/python/stri.py",
    "filename": "stri.py",
    "code": "str =\"New Delhi is capital of India Bengaluru is capital of Karnataka\"\nwordCount=len(str.split())\nprint(\"Total Number of words : \", wordCount)#print the word count\ncounts = dict()# Create an empty dictionary\nwords = str.split()\nfor word in words:\n\tif word in counts:\n\t\tcounts[word] =counts[word]+ 1\n\telse:\n\t\tcounts[word] = 1\nfor key in list(counts.keys()):\n\tprint(key, \":\", counts[key])\nsearchWord=input(\"Enter the word to search : \")\nresult = str.find(searchWord)\nif(result!=-1):#if Found disply success message\n\tprint(searchWord +\" Word found in string\")\nelse:#if not Found disply unsuccessfull message\n\tprint(searchWord + \" !!!!! Word not found in string\")\n",
    "created": "2025-11-09T13:25:08.356785"
  },
  {
    "id": "python_47",
    "language": "python",
    "title": "Strings",
    "description": "Migrated from templates/code_samples/python/strings.py",
    "filename": "strings.py",
    "code": "name=\"skibidi\"\nshort=name[-3:-1] # same as 1 to 3 excluding 2\nprint(short)\nchar1=name[-3]\nprint(char1)\nprint(len(name))",
    "created": "2025-11-09T13:25:08.356785"
  },
  {
    "id": "python_48",
    "language": "python",
    "title": "Sumn",
    "description": "Migrated from templates/code_samples/python/sumn.py",
    "filename": "sumn.py",
    "code": "n=int(input(\"Enter the number:\"))\ni=1\nsum=0\nwhile(i<=n):\n    sum+=i\n    i+=1\nprint(sum)",
    "created": "2025-11-09T13:25:08.356785"
  },
  {
    "id": "python_49",
    "language": "python",
    "title": "Swggame",
    "description": "Migrated from templates/code_samples/python/swggame.py",
    "filename": "swggame.py",
    "code": "'''\ns=1\nw=-1\ng=0\n'''\ncomp = -1  # Let's say -1 represents \"Water\"\nyou_input = input(\"Enter your attack mode (Snake/Water/Gun): \")\n\n# Define the choices\nyouD = {\"Snake\": 1, \"Water\": -1, \"Gun\": 0}\n\n# Check if user input is valid\nif you_input not in youD:\n    print(\"Invalid input. Please choose from Snake, Water, or Gun.\")\nelse:\n    you = youD[you_input]\n\n    if comp == you:\n        print(\"The game is a draw.\")\n    elif (comp == -1 and you == 1) or (comp == 0 and you == -1) or (comp == 1 and you == 0):\n        print(\"You win!\")\n    else:\n        print(\"You lose!\")\n",
    "created": "2025-11-09T13:25:08.356785"
  },
  {
    "id": "c_0",
    "language": "c",
    "title": "01 Pointer",
    "description": "Code file: 01_pointer.c",
    "filename": "01_pointer.c",
    "code": "#include <stdio.h>\n\nint main(){\n    int j=45;\n    int* k=&j;// k is a pouner pointing to j\n    int metaman=99;\n    int x=10000;\n    int* beta=&x;\n    printf(\"%p\\n\",&x);\n    printf(\"%d\\n\",*(&x));\n    printf(\"%u\\n\",*beta);\n    printf(\"%u\\n\",&j);\n    printf(\"%p\\n\",&k);// Every variable has its address \n    printf(\"The address of %d is %p in hexadecimals\\n\",j,&j);\n    // printf(\"%u in hexadecimals\\n\",j,&j);\n    printf(\"\\nThe Address is %p\\n\",k);\n    printf(\"%p\",&metaman);\n    printf(\"\\nThe value of address j is %d\\n\",*(&j));\n    printf(\"\\nThe value of address j is %d\",*k);\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_1",
    "language": "c",
    "title": "02 Func",
    "description": "Code file: 02_func.c",
    "filename": "02_func.c",
    "code": "#include <stdio.h>\n\nint change(int a);\n\nint change(int a){\n    a=44; // Misnomer\n    return 0;\n}\n\nint main(){\n    int b=22;\n    int c;\n    change(b); // b remains 22 it only gives copies\n    printf(\"b is %d\\n\", b);\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_2",
    "language": "c",
    "title": "02 Inout",
    "description": "Code file: 02_inout.c",
    "filename": "02_inout.c",
    "code": "#include <stdio.h>\n\nint main(){\n    int marks[5];\n    printf(\"Enter marks of 5 students\\n\");\n    // scanf(\"%d\",&marks[0]);\n    // scanf(\"%d\",&marks[1]);\n    // scanf(\"%d\",&marks[2]);\n    // scanf(\"%d\",&marks[3]);\n    // scanf(\"%d\",&marks[4]);\n    for(int i=0;i<5;i++){\n        scanf(\"%d\",&marks[i]);\n    }\n     for(int i=0;i<5;i++){\n        printf(\"Value of marks at index %d is %d\\n\",i,marks[i]);\n     }\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_3",
    "language": "c",
    "title": "Area",
    "description": "Code file: area.c",
    "filename": "area.c",
    "code": "#include <stdio.h>\n#include <math.h>\n\nint main(){\n    float side=4.12;\n    printf(\"The area of the square is %0.2f\", pow(side,2));\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_4",
    "language": "c",
    "title": "Array",
    "description": "Code file: array.c",
    "filename": "array.c",
    "code": "#include <stdio.h>\n\nint main(){\n    int marks[90]; // reserve space to store 90 integers in 90 elements 0 to 89\n    marks[0]=95;\n    marks[1]=90;\n    // We can go alll the way till marks[89]\n    printf(\"%d and %d\", marks[0],marks[0]);\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_5",
    "language": "c",
    "title": "Array2D",
    "description": "Code file: array2d.c",
    "filename": "array2d.c",
    "code": "#include <stdio.h>\n\nint main(){\n    int array[3][2];\n    for (int i=0;i<3;i++){\n         for (int j=0;j<2;j++)\n         {\n            printf(\"Enter the value of array[%d][%d]\\n\",i,j);\n            scanf(\"%d\",&array[i][j]);\n         }\n    }\n    for (int i=0;i<3;i++){\n        for(int j=0;j<2;j++){\n            printf(\"The value of array[%d][%d] is %d\\n\",i,j,array[i][j]);\n        }\n    }\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_6",
    "language": "c",
    "title": "Array2D2",
    "description": "Code file: array2d2.c",
    "filename": "array2d2.c",
    "code": "#include <stdio.h>\n\nint main(){\n    int marks[2][2]={2,4,5,6};\n    for(int i=0;i<2;i++){\n        for(int j=0;j<2;j++){\n            printf(\"%d \",marks[i][j]);\n        }\n        printf(\"\\n\");\n    }\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_7",
    "language": "c",
    "title": "Arraysinmem",
    "description": "Code file: arraysinmem.c",
    "filename": "arraysinmem.c",
    "code": "#include <stdio.h>\n\nint main(){\n    int marks[5];\n    printf(\"Enter marks of 5 students\\n\");\n    // scanf(\"%d\",&marks[0]);\n    // scanf(\"%d\",&marks[1]);\n    // scanf(\"%d\",&marks[2]);\n    // scanf(\"%d\",&marks[3]);\n    // scanf(\"%d\",&marks[4]);\n    for(int i=0;i<5;i++){\n        scanf(\"%d\",&marks[i]);\n    }\n     for(int i=0;i<5;i++){\n        printf(\"The address of marks at index %d is %u\\n\",i,&marks[i]); // difference of 4 in each address of the blocks in arrays always like this u can change the pointer pointing element change elements by mem address +i ptr++ etc\n     }\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_8",
    "language": "c",
    "title": "Arrayusingpointers",
    "description": "Code file: arrayusingpointers.c",
    "filename": "arrayusingpointers.c",
    "code": "#include <stdio.h>\n\nint main(){\n    int marks[]={122,123,125,143};\n    int *ptr=&marks[0]; // or use int *ptr =marks; for 1st elements \n    for (int i=0;i<4;i++){\n        printf(\"The marks at %d is %d\\n\",i,marks[i]);\n        printf(\"The marks at index %d is %d\\n\",i,*ptr);\n        ptr++;\n    }\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_9",
    "language": "c",
    "title": "Callbyref",
    "description": "Code file: callbyref.c",
    "filename": "callbyref.c",
    "code": "#include <stdio.h>\n\nint s(int *,int *);\n\n// Sum should change value of a\nint s(int* x, int* y){\n    *x=6;\n    return *x+*y;\n}\nint main(){\n    int a=1,b=2;\n    s(&a,&b); //\n    printf(\"The value of a is %d\",a);\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_10",
    "language": "c",
    "title": "Callbyvalue",
    "description": "Code file: callbyvalue.c",
    "filename": "callbyvalue.c",
    "code": "#include <stdio.h>\n\nint s(int,int);\n\nint s(int x, int y){\n    return x+y;\n}\nint main(){\n    s(1,2); //\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_11",
    "language": "c",
    "title": "Dec For Loop",
    "description": "Code file: dec_for_loop.c",
    "filename": "dec_for_loop.c",
    "code": "#include <stdio.h>\n\nint main(){\n    for (int i = 15; i>=0; i--){\n        if(i==5){\n            break; // Exit the loop when i is 5\n        }\n        printf(\"The value of i is %d\\n\", i); // Prints values from 15 to 6  \n    }\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_12",
    "language": "c",
    "title": "File",
    "description": "Code file: file.c",
    "filename": "file.c",
    "code": "#include <stdio.h>\n\nint main(){\n    FILE *ptr;\n    ptr=fopen(\"harry.txt\",\"r\");\n    int num;\n    fscanf(ptr,\"%d\",&num);\n    printf(\"Value of num is %d\\n\",num);\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_13",
    "language": "c",
    "title": "Fileopen",
    "description": "Code file: fileopen.c",
    "filename": "fileopen.c",
    "code": "#include <stdio.h>\n\nint main(){\n    \n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_14",
    "language": "c",
    "title": "Filequiz",
    "description": "Code file: filequiz.c",
    "filename": "filequiz.c",
    "code": "#include <stdio.h>\n\nint main(){\n    FILE *ptr;\n    ptr=fopen(\"harry.txt\",\"r\");\n    int num;\n    fscanf(ptr,\"%d\",&num);\n    printf(\"Value of printf is %d \\n\",num);\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_15",
    "language": "c",
    "title": "Fnrstrings",
    "description": "Code file: fnrstrings.c",
    "filename": "fnrstrings.c",
    "code": "#include <stdio.h>\n#include <string.h>\n\nint main(){\n    char st[]=\"Harry\";\n    char a1[56]=\"Harry\";\n    char a2[56]=\"Bhai-\";\n    printf(\"%u\",st);\n    // printf(\"%ld\",strlen(st)); // excluding null chr\n    char target[30];\n    strcpy(target,st);\n    // printf(\"%s %s\",st,target);\n    strcat(a1,a2); // a1 now contains harrybhai\n    printf(\"%s %s\",a1,a2);\n    int a=strcmp(\"far\",\"ajoke\"); // give positibe if ajoke comes first acc to dictironary and gives negative value if the far comes first \n    printf(\"%d\",a);\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_16",
    "language": "c",
    "title": "Func",
    "description": "Code file: func.c",
    "filename": "func.c",
    "code": "#include <stdio.h>\n\nvoid display();\n\nint main(){\n    int a; // void means returns nothing variable declaration\n    display(); // Fn call\n    return 0;\n}\n\n// Fn definition\nvoid display(){\n    printf(\"hi i am a display\\n\");\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_17",
    "language": "c",
    "title": "Gets",
    "description": "Code file: gets.c",
    "filename": "gets.c",
    "code": "#include <stdio.h>\n\nint main(){\n    char st[30];\n    gets(st); // for multiword the entered string gets stored in st\n    printf(\"%s\",st);\n    // puts(st);\n    printf(\"hey\");\n    return 0;\n}\n\n//gets is dangerous becuase of buffer overflow and deprecated",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_18",
    "language": "c",
    "title": "Inputs",
    "description": "Code file: inputs.c",
    "filename": "inputs.c",
    "code": "#include <stdio.h>\n\nint main(){\n    char st[4]; \n    scanf(\"%s\",st); // or &st[0] scanf add null already so no need of \\n cant use multiword or spcases string must  big enough to fit it \n    printf(\"%s\",st);\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_19",
    "language": "c",
    "title": "Otherinitwaysofarrays",
    "description": "Code file: otherinitwaysofarrays.c",
    "filename": "otherinitwaysofarrays.c",
    "code": "#include <stdio.h>\n\nint main(){\n    int cgpa[]={9,8,8}; // you can put 3 or leave empty\n     for(int i=0;i<3;i++){\n        printf(\"Value of arrays at index %d is %d\\n\",i,cgpa[i]);\n     }\n    return 0;\n}\n\n// each arrays take 4 bytes meaning 1 takes 62302 to 62305",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_20",
    "language": "c",
    "title": "P1",
    "description": "Code file: p1.c",
    "filename": "p1.c",
    "code": "#include <stdio.h>\n\nint avg(int,int,int);\n\nint avg(int x,int y,int z){\n    return (x+y+z)/3;\n}\nint main(){\n    int n1,n2,n3;\n    printf(\"Enter Number 1:\");\n    scanf(\"%d\",&n1);\n    printf(\"Enter Number 2:\");\n    scanf(\"%d\",&n2);\n    printf(\"Enter Number 3:\");\n    scanf(\"%d\",&n3);\n    printf(\"Average of these 3 numbers is %d\", avg(n1,n2,n3));\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_21",
    "language": "c",
    "title": "P2",
    "description": "Code file: p2.c",
    "filename": "p2.c",
    "code": "#include <stdio.h>\n\nfloat ctof(float);\n\nfloat ctof(float x){ // important thing\n    return (9.0/5.0)*x+32;\n}\nint main(){\n    float n;\n    printf(\"Enter celsius value to convert it to fahreinheat: \\n\");\n    scanf(\"%f\",&n);\n    printf(\"%0.2f F\",ctof(n));\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_22",
    "language": "c",
    "title": "P3",
    "description": "Code file: p3.c",
    "filename": "p3.c",
    "code": "#include <stdio.h>\n\nvoid printArray(int a[],int n){\n    for(int i=0;i<n;i++){\n        printf(\"%d\",a[i]);\n    }\n    printf(\"\\n\");\n}\n\nvoid reverse(int arr[],int n){\n    int temp;\n    for (int i=0;i<n/2;i++){\n        temp=arr[i];\n        arr[i]=arr[n-i-1];\n        arr[n-i-1]=temp;\n    }\n}\nint main(){\n    int arr[]={1,2,3,4,5,6};\n    printArray(arr,6);\n    reverse(arr,6);\n    printArray(arr,6);\n    return 0;\n}\n\n// temp=a a=b b=temp\n// 0 to 5 \n// 1 to 4 and 2 to 3\n// i from 0 to n/2\n// arr[i] to arr[n-i-1]",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_23",
    "language": "c",
    "title": "P4",
    "description": "Code file: p4.c",
    "filename": "p4.c",
    "code": "#include <stdio.h>\n\nvoid npia(int a[],int n){\n    int no_of_positive=0;\n    for(int i=0;i<n;i++){\n        if(a[i]>0){\n            no_of_positive ++; //int temp[]={a[i]};\n        }\n    }\n    printf(\"The number of positive integers in the given array is %d \", no_of_positive);\n}\nint main()\n{\n    int array[] = {-1, -2, -3, -4, -5, -6, -7, -8, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10};\n    npia(array,19);\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_24",
    "language": "c",
    "title": "P5",
    "description": "Code file: p5.c",
    "filename": "p5.c",
    "code": "#include <stdio.h>\n\nint main(){\n    int n1,n2,n3;\n    scanf(\"%d %d %d\",&n1,&n2,&n3);\n    int arr[3][10];\n    int mul[]={n1,n2,n3};\n    for (int i=0;i<3;i++){\n        for(int j=0;j<10;j++){\n            arr[i][j]=mul[i]*(j+1);\n        }\n    }\n    for (int i=0;i<3;i++){\n        for(int j=0;j<10;j++){\n            printf(\"The value of arr[%d][%d] is %d\\n\",i,j,arr[i][j]);\n        }\n        printf(\"\\n\");\n    }\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_25",
    "language": "c",
    "title": "P6",
    "description": "Code file: p6.c",
    "filename": "p6.c",
    "code": "#include <stdio.h>\n\nint main(){\n    int arr[2][3][4];\n    for (int i=0;i<2;i++){\n        for(int j=0;j<3;j++){\n            for(int k=0;k<4;k++){\n            printf(\"%u\\n\",&arr[i][j][k]);\n            }}}\n\n    return 0;\n        }",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_26",
    "language": "c",
    "title": "P7 Decrept",
    "description": "Code file: p7_decrept.c",
    "filename": "p7_decrept.c",
    "code": "#include <stdio.h>\n#include <string.h>\n\nint main(){\n    char str[]=\"Ifmmp!vtfs!xfmdpnf!\";\n    for(int i=0;i<strlen(str);i++)\n    {\n        str[i]=str[i]-1;\n    }\n    printf(\"%s\",str);\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_27",
    "language": "c",
    "title": "P8",
    "description": "Code file: p8.c",
    "filename": "p8.c",
    "code": "#include <stdio.h>\n#include <string.h>\n\nint main(){\n    char c='r';\n    int count=0;\n    char str[]=\"Harry\";\n    for(int i=0;i<strlen(str);i++)\n    {\n        if(str[i]==c){\n            count++;\n        }\n    }\n    printf(\"%d\",count);\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_28",
    "language": "c",
    "title": "Pointertopointer",
    "description": "Code file: pointertopointer.c",
    "filename": "pointertopointer.c",
    "code": "#include <stdio.h>\n\nint main(){\n    int i=5;\n    int *j=&i;\n    int **k=&j;\n// ***&&&a =a cancels out\n    printf(\"The value of i is %d\\n\", **k); // i *j *(&i) **k ***w **(&j) .....\n    printf(\"The value of i is %d\\n\", **(&j));\n    return 0;\n}\n\n//FUctions calls\n/*\n1. Call by value: sending values of arguments\n2. call by reference: sending the address of arguments\n\n*/",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_29",
    "language": "c",
    "title": "Strings",
    "description": "Code file: strings.c",
    "filename": "strings.c",
    "code": "#include <stdio.h>\n\nint main(){\n    // char st[]={'a','b','c','\\0'};\n    char st[]=\"abc\";\n    // for(int i=0;i<3;i++){\n    //     printf(\"The char is %c\\n\",st[i]);\n    // }\n    printf(\"First character is %s \\n\", st);\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.801764"
  },
  {
    "id": "c_30",
    "language": "c",
    "title": "Structures",
    "description": "Code file: structures.c",
    "filename": "structures.c",
    "code": "#include <stdio.h>\n#include <string.h>\n#include <math.h>\n\nstruct employee\n{\n    int code;// This declares a new user defined data type\n    float salary;\n    char name[10];\n}; //semiclon is important\n\nint main(){\n    struct employee e1,e2;\n    strcpy(e1.name,\"Harry\");\n    e1.code=4511;\n    e1.salary=54.44;\n    printf(\"%d %f %s\", e1.code,e1.salary,e1.name);\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.802764"
  },
  {
    "id": "c_31",
    "language": "c",
    "title": "Struput",
    "description": "Code file: struput.c",
    "filename": "struput.c",
    "code": "#include <stdio.h>\n#include <string.h>\n\nstruct employee\n{\n    int code;// This declares a new user defined data type\n    float salary;\n    char name[10];\n}; //semiclon is important\n\nint main(){\n    struct employee e1,e2,e3;\n    strcpy(e1.name,\"Harry\");\n    e1.code=4511;\n    e1.salary=54.44;\n    printf(\"%d %f %s\", e1.code,e1.salary,e1.name);\n    return 0;\n}",
    "created": "2025-11-16T06:32:59.802764"
  },
  {
    "id": "c_32",
    "language": "c",
    "title": "Hello",
    "description": "Code file: hello.c",
    "filename": "hello.c",
    "code": "#include <stdio.h>\n\nint main() {\n    printf(\"Hello, World!\\n\");\n    return 0;\n}\n",
    "created": "2025-11-16T06:41:28.796630"
  },
  {
    "id": "cpp_0",
    "language": "cpp",
    "title": "Struct",
    "description": "Migrated from templates/code_samples/cpp/struct.cpp",
    "filename": "struct.cpp",
    "code": "#include <iostream>\n\nclass Dog{\n    std::string name;\n}; // Members are private by default\n\nstruct Cat{\n    std::string name;\n}; // Members are public by default \n// Members can be made private or protected using access specifiers\n\nstruct Point{\n    double x;\n    double y;\n};\n\nint main(){\n    Dog dog1;\n    Cat cat1;\n    // dog1.name = \"Buddy\"; // Error: 'name' is private within this context\n    cat1.name = \"Whiskers\"; // OK: 'name' is public within this context\n    std::cout << \"Cat's name: \" << cat1.name << std::endl;\n    Point p1;\n    p1.x = 10.5;\n    p1.y = 20.5;\n    std::cout << \"Point coordinates: (\" << p1.x << \", \" << p1.y << \")\" << std::endl;\n    return 0;\n}",
    "created": "2025-11-09T13:25:08.354785"
  },
  {
    "id": "cpp_1",
    "language": "cpp",
    "title": "Templatebyref",
    "description": "Migrated from templates/code_samples/cpp/templatebyref.cpp",
    "filename": "templatebyref.cpp",
    "code": "#include <iostream>\n\ntemplate <typename T> \nconst T& maximum(const T& a,const T& b){\n    std::cout << &a << std::endl;\n    return (a>b)?a:b;\n}\nint main(){\n    int a{1};\n    int b{2};\n    std::cout << &a << std::endl;\n    auto result=maximum(a,b);    \n    std::cout << &a << std::endl;\n    std::cout << result << std::endl;\n    return 0;\n}\n\n// while in pass by value addresses inside and outside are different while inside its same in ref",
    "created": "2025-11-09T13:25:08.354785"
  },
  {
    "id": "cpp_2",
    "language": "cpp",
    "title": "Templatefn",
    "description": "Migrated from templates/code_samples/cpp/templatefn.cpp",
    "filename": "templatefn.cpp",
    "code": "#include <iostream>\n#include <string>\n\ntemplate <typename T>\nT maximum(T a,T b){\n    return (a>b)?a:b;\n}\n\nint main(){\n    int c{9};\n    int d{10};\n    double pie{3.14};\n    double e{2.718};\n    std::string s1{\"All Hail\"};  \n    std::string s2{\"Lelouch\"};\n    auto result = maximum(c,d);\n    std::cout << result << std::endl;\n    // Explicit template arguments\n    maximum<double>(c,e); // Converts int to double  as it is implicit conversion \n    maximum<double>(c,d); // explicitly say that we want the double \n    // version called ,if an instance is not there\n    // already it will be created\n    //maximum<double>(a,e); // error : compiler error as cant convert string to double \n    return 0;\n}\n\n// we cant do templates on ptr bcs compiler will compare the addresses instead of values and cayses problems",
    "created": "2025-11-09T13:25:08.354785"
  },
  {
    "id": "cpp_3",
    "language": "cpp",
    "title": "Templatespecialization",
    "description": "Migrated from templates/code_samples/cpp/templatespecialization.cpp",
    "filename": "templatespecialization.cpp",
    "code": "#include <iostream>\n#include <cstring>\n\ntemplate <typename T>  T maximum(T a,T b){\n    return (a>b)?a:b;\n}\ntemplate <>\nconst char* maximum<const char*> (const char* a,const char* b){\n    return (std::strcmp(a,b)>0)?a:b;\n}\nint main(){\n    // int a{10};\n    // int b{23};\n    // double c{344.44};\n    // double d{453.45};\n    std::string e{\"hakai\"};\n    std::string f{\"world\"};\n    // auto max_int = maximum(a,b);\n    const char* l{\"lmao\"};\n    const char* s{\"Disaster\"};\n    const char* res=maximum(l,s);\n    std::cout << res << std::endl;\n    return 0;\n}\n",
    "created": "2025-11-09T13:25:08.354785"
  },
  {
    "id": "cpp_4",
    "language": "cpp",
    "title": "Thisptr",
    "description": "Migrated from templates/code_samples/cpp/thisptr.cpp",
    "filename": "thisptr.cpp",
    "code": "#include <iostream>\n#include <string_view>\n\nclass Dog{\n    public:\n        Dog() = default;\n        Dog(std::string_view name_param,std::string_view breed_param,int age_param );\n        ~Dog();\n\n        void print_info(){\n            std::cout << \"Dog (\" << this << \") : [ name : \" << name << \" Breed : \" << breed << \" Age : \" << *p_age << \"]\" << std::endl;\n        }\n        //Setters\n        Dog& set_name(std::string_view name){\n            this->name=name; // name=name not good\n            return *this;\n        }\n        Dog& set_breed(std::string_view breed){\n            this->breed=breed; // name=name not good\n            return *this;\n        }\n        Dog& set_age(int age){\n            *(this->p_age)=age; // name=name not good\n            return *this;\n        }\n\n    private:\n        std::string name;\n        std::string breed;\n        int* p_age{nullptr};\n};\nDog::Dog(std::string_view name_param,std::string_view breed_param,int age_param){\n    name=name_param;\n    p_age=new int;\n    breed=breed_param;\n    *p_age=age_param;\n    std::cout << \"Dog constructor called for: \" << name  << \" at \" << this << std::endl;\n\n}\n\nDog::~Dog(){\n    delete p_age;\n    std::cout << \"Dog destructor called for: \" << name  << \" at  \" << this << std::endl;\n}\n\nint main(){\n    Dog dog1(\"SSDXCD\",\"Sheperfd\",4); // constructor\n    dog1.print_info();\n    // dog1.set_name(\"Puma\");\n    // dog1.set_age(65);    \n    // Chained calls using ptr\n    // dog1.set_name(\"Lumba\")->set_breed(\"Wolf breed\") ->set_age(4);\n    // Chained calls using references  \n    dog1.set_name(\"Lumba\").set_breed(\"Wolf breed\").set_age(4);\n\n\n    dog1.print_info();\n    std::cout << \"done\" << std::endl;\n    return 0;\n}",
    "created": "2025-11-09T13:25:08.354785"
  },
  {
    "id": "cpp_5",
    "language": "cpp",
    "title": "Weirdintegraltypes",
    "description": "Migrated from templates/code_samples/cpp/weirdintegraltypes.cpp",
    "filename": "weirdintegraltypes.cpp",
    "code": "#include <iostream>\n\nint main(){\n    short int var1{10};\n    short int var2{20}; // 2byt \n    char var3{34}; // 1byt \n    char var4{44};\n    // < 4 bytes no no arithmatic operations\n    std::cout << sizeof(var1) << std::endl;\n    auto result1= var1+var2;\n    auto r2=var3+var4;\n    std::cout << result1 << '\\n' << r2 << \"\\n\" << sizeof(r2) << \"\\n\" << sizeof(result1) << std::endl;\n    return 0;\n}",
    "created": "2025-11-09T13:25:08.354785"
  },
  {
    "id": "html_0",
    "language": "html",
    "title": "Css3d",
    "description": "Migrated from templates/code_samples/html/css3d.html",
    "filename": "css3d.html",
    "code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Transforms</title>\n    <style>\n        .master{\n            height:455px;\n            background-color: brown;\n        }\n        .box{\n            display:inline-block;\n            border: 3px solid black;\n            /* transform:translate(23px) rotate(34deg) ;\n            transform-origin:0;\n            transform:scaleX(3px);\n            transform:matrix3d(1,2,3,4,5,6); */\n        }\n        img{\n            width:56px;\n            height:34px;\n            /* transition-property: width;\n            transition-duration: 3s;\n            transition-timing-function: ease-in;\n            transition-delay:1s ; */\n            transition: width 3s ease-in 1s,height 4s ease-in;\n        }\n        img:hover{\n            width:996px;\n            height:996px;\n        }\n\n    </style>\n</head>\n<body>\n    <div class=\"master\">\n        <div class=\"box\"><img src=\"1.png\" alt=\"\"></div>\n        \n    </div>\n</body>\n</html>",
    "created": "2025-11-09T13:25:08.354785"
  },
  {
    "id": "html_1",
    "language": "html",
    "title": "Cssgrid",
    "description": "Migrated from templates/code_samples/html/cssgrid.html",
    "filename": "cssgrid.html",
    "code": "<!DOCTYPE html>\n<html lang=\"en\">\n\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Document</title>\n    <style>\n        .container{\n            display: grid;\n            background-color: aqua;\n            grid-template-columns: auto auto auto auto;\n            /* grid-row-gap: 10px;\n            grid-column-gap: 10px; */\n            /* grid-gap: 2px 9px; */\n            grid-gap:10px;\n            height:1000px;\n            padding: 10px;\n            border: 2px solid black;    \n        }\n        .item{\n            background-color: chocolate;\n            color: beige;\n        }\n    </style>\n</head>\n\n<body>\n    <div class=\"container\">\n        <div class=\"item\" style=\"grid-row:span 3\">1</div>\n        <div class=\"item\">2</div>\n        <div class=\"item\"style=\"grid-column:1/3\">3</div>\n        <div class=\"item\">4</div>\n        <div class=\"item\">5</div>\n        <div class=\"item\">6</div>\n        <div class=\"item\">7</div>\n        <div class=\"item\">8</div>\n        <div class=\"item\">9</div>\n        <div class=\"item\">10</div>\n        <div class=\"item\">11</div>\n        <div class=\"item\">12</div>\n        <div class=\"item\">13</div>  \n        <div class=\"item\">14</div>\n        <div class=\"item\">15</div>\n        <div class=\"item\">16</div>\n        <div class=\"item\">17</div>\n        <div class=\"item\">18</div>\n        <div class=\"item\">19</div>\n        <div class=\"item\">20</div>\n        <div class=\"item\">21</div>\n        <div class=\"item\">22</div>\n        <div class=\"item\">23</div>\n        <div class=\"item\">24</div>\n        <div class=\"item\">25</div>\n        <div class=\"item\">26</div>\n        <div class=\"item\">27</div>\n        <div class=\"item\">28</div>\n        <div class=\"item\">29</div>\n        <div class=\"item\">30</div>\n    </div>\n</body>\n\n</html>",
    "created": "2025-11-09T13:25:08.354785"
  },
  {
    "id": "html_2",
    "language": "html",
    "title": "Flexbox",
    "description": "Migrated from templates/code_samples/html/flexbox.html",
    "filename": "flexbox.html",
    "code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width\n    initial-scale=1.0\">\n    <title>Float</title>\n    <style>\n        .container{\n            display: flex;\n            flex-direction:row;\n            font-size:72px;\n            font-weight: 900;\n            height:60vh;\n            /* flex-wrap: wrap; */\n            background-color: blue;\n            justify-content: space-between;\n            align-items: center;\n        }\n        .b1{\n            height:373px;\n            width: 444px;\n            font-weight: 900;\n            flex-grow: initial;\n            background-color: aqua;\n            border: 4px sollid red;\n\n        }\n        .b2{ height:373px;\n            width: 444px;\n            background-color: red;\n            border: 4px solid black\n        }\n    </style>\n</head>\n<body>\n    <div class=\"container\">\n        <div class=\"b1\">b1</div>\n        <div class=\"b2\">b2</div>\n        <div class=\"b2\">b3</div>\n        <div class=\"b2\">b4</div>\n    </div>\n</body>\n</html>",
    "created": "2025-11-09T13:25:08.354785"
  },
  {
    "id": "html_3",
    "language": "html",
    "title": "P1",
    "description": "Migrated from templates/code_samples/html/p1.html",
    "filename": "p1.html",
    "code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Document</title>\n    <style>\n        *{margin: 0;\n        padding: 0;}\n        .user{\n            width:100%;\n            height:14px;\n            background-color: black;\n        }\n        .boss{\n            width:49.5999%;\n            height:60vh;\n            background-color: red;\n            display: inline-block;\n        }\n        .master{\n            display: inline-block;\n            width: 50%;\n            height:60vh;\n            background-color: green;\n        }\n    </style>\n</head>\n<body>\n    <div class=\"user\"></div>\n    <div class=\"boss\"></div>\n    <div class=\"master\"></div>\n</body>\n</html>",
    "created": "2025-11-09T13:25:08.354785"
  },
  {
    "id": "html_4",
    "language": "html",
    "title": "P2",
    "description": "Migrated from templates/code_samples/html/p2.html",
    "filename": "p2.html",
    "code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Float</title>\n    <style>\n        .b1{\n            height:373px;\n            width: 444px;\n            background-color: blue;\n            float: left;\n        }\n        .b2{ height:373px;\n            width: 444px;\n            background-color: red;\n            float: inherit;\n        }\n    </style>\n</head>\n<body>\n    <div class=\"b1\">b1</div>\n    <div class=\"b2\">b2</div>\n</body>\n</html>",
    "created": "2025-11-09T13:25:08.354785"
  },
  {
    "id": "html_5",
    "language": "html",
    "title": "Playout",
    "description": "Migrated from templates/code_samples/html/playout.html",
    "filename": "playout.html",
    "code": "<!DOCTYPE html>\n<html lang=\"en\">\n\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Layout</title>\n    <style>\n        * {\n            margin: 0;\n            padding: 0;\n        }\n\n        li {\n            list-style: none;\n            display: inline;\n            font-size: large;\n            border: 4px solid red;\n            border-radius: 0ric;\n        }\n\n        ul {\n            padding: 34px;\n        }\n\n        header {\n            display: flex;\n            flex-direction: row;\n            justify-content: end;\n            background-color: black;\n            color: white;\n            width: 100vw;\n        }\n\n        .image {\n            background-image: url(2.png);\n            height: 100px;\n            width: 100vw;\n        }\n\n        .container {\n            background-color: chocolate;\n            height: 699px;\n            width: 100vw;\n            display: flex;\n            flex-direction: row;\n            justify-content: space-around;\n            border: 16px solid chocolate;\n        }\n\n        .b1 {\n            background-image: url(1.png);\n            height: 578px;\n            width: 30vw;\n        }\n\n        .b2 {\n            background-image: url(2.png);\n            height: 578px;\n            width: 30vw;\n        }\n\n        .b3 {\n            background-image: url(3.png);\n            height: 578px;\n            width: 30vw;\n        }\n    </style>\n</head>\n\n<body>\n    <header>\n        <nav>\n            <ul>\n                <li>Home</li>\n                <li>About</li>\n                <li>Contact</li>\n            </ul>\n        </nav>\n    </header>\n    <div class=\"image\"></div>\n    <div class=\"container\">\n        <div class=\"b1\"></div>\n        <div class=\"b2\"></div>\n        <div class=\"b3\"></div>\n    </div>\n</body>\n\n</html>",
    "created": "2025-11-09T13:25:08.354785"
  },
  {
    "id": "html_6",
    "language": "html",
    "title": "Text",
    "description": "Migrated from templates/code_samples/html/text.html",
    "filename": "text.html",
    "code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Document</title>\n</head>\n<body>\n    <header>This is fun</header>\n    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorum enim veniam itaque hic accusantium a consequatur consequuntur nobis voluptas. Quia, officiis id, hic doloremque eaque, natus recusandae itaque necessitatibus consequuntur consectetur assumenda amet ea. Voluptates facere, ducimus cupiditate quas non dolores minima aspernatur quidem, quisquam vel labore, iure expedita suscipit rerum. Aliquid qui a eligendi? Recusandae exercitationem placeat delectus! Nihil exercitationem sed tempore atque cum saepe dicta! Ratione incidunt fuga fugiat soluta a praesentium voluptates eum? Beatae velit, error repudiandae esse tempore vero, temporibus nulla quisquam quidem aliquid corrupti consequatur dolorem iste ipsum id dolore saepe atque iure. Et, officia quia? Magni ad perferendis voluptas dolores alias nostrum similique saepe, laudantium sequi beatae sint consequuntur? Enim reprehenderit doloribus quo dicta? Nesciunt atque quam praesentium. Laborum natus reprehenderit nulla debitis quidem perferendis commodi ex fuga labore. At ad nesciunt sequi natus suscipit praesentium dolorem, tempora alias minima magnam harum, et repellat neque, eligendi eos possimus numquam! Eum labore aliquid reprehenderit consequatur exercitationem? Possimus, ex? Iste, iusto voluptas reiciendis natus itaque in, doloremque nam aut architecto tenetur sint vel eaque. Voluptate voluptatum, eligendi maxime itaque cumque voluptas, ad non doloremque voluptatibus quia illo fugit laborum molestias quae ipsa veniam praesentium at. Natus, animi, molestiae, facere atque voluptate excepturi illum quas doloribus quod alias est culpa. Fuga dolor esse repudiandae possimus officiis ab dicta odit voluptatem aspernatur at neque rerum autem vel iste dolorum quidem sunt enim, commodi doloremque, cupiditate molestias totam perspiciatis. Odio veritatis mollitia facere perferendis impedit doloremque ipsum voluptatem reiciendis, ut itaque rerum tempora nisi eaque dolorem sit, eius nesciunt necessitatibus neque in quos. Ducimus quo dignissimos optio fugit amet iusto perspiciatis minima consectetur praesentium corrupti beatae, laborum fugiat veritatis blanditiis. Facilis mollitia recusandae quia libero, asperiores, totam corporis magnam incidunt corrupti quis molestiae eligendi neque. Accusantium, assumenda quae ducimus animi fugit harum sed officiis quos. Sint obcaecati quo porro quaerat animi culpa reprehenderit blanditiis quas, dolorem, aut ex repudiandae est expedita, totam autem vel laboriosam nostrum non. Inventore officia harum rem sint quibusdam numquam, modi eius praesentium necessitatibus ab cum commodi consequuntur voluptates consectetur illo aperiam labore asperiores. Amet obcaecati hic, ab temporibus, in, deleniti doloremque nulla facere sequi enim ea facilis deserunt voluptatibus optio consectetur. Saepe accusamus pariatur repudiandae debitis? Dolor exercitationem repellat labore perspiciatis soluta placeat pariatur ipsa quis esse iusto similique natus quod blanditiis, adipisci culpa alias cum, explicabo voluptas atque animi a deleniti id? Itaque ducimus iste aliquam! Recusandae saepe, velit tenetur sint ipsam esse atque ab numquam est iure, explicabo debitis laboriosam dolore iusto nam maiores? Et, aspernatur quasi voluptates officiis iste adipisci odio enim hic debitis. Non dolorum voluptates asperiores veritatis quibusdam obcaecati, quos esse minus culpa totam ad ducimus nisi fuga in explicabo incidunt eaque enim iusto aut. Maiores blanditiis alias rerum vitae praesentium laboriosam, sapiente quidem eos nulla eaque maxime natus expedita ipsum quos atque. Quam dolores repudiandae error veritatis perspiciatis ab explicabo maiores corporis porro ipsum ad culpa non tenetur, velit tempora laborum sint odio incidunt? Nisi, ab. Delectus natus exercitationem voluptas itaque eius tenetur quo quasi ipsa minus ab aut voluptatibus similique doloribus placeat unde, maiores amet distinctio libero non dolore repellendus voluptatem eos nihil? Doloribus inventore architecto distinctio, consequatur omnis cupiditate dignissimos quod autem optio accusantium quasi ut enim nihil, sunt vero deleniti magni illo repellendus tempora velit provident eius. Obcaecati quidem, dolorum quo, nihil tempore aliquid molestiae quae exercitationem ducimus maxime sunt sint omnis, nisi magnam eum quod perferendis in inventore provident consectetur! Nam atque cum veritatis fugiat quos corrupti, rem labore, delectus quo aperiam dolore numquam quas earum neque nemo quod vel eius explicabo omnis quasi enim, impedit tempora. Illo, odit? Qui dolorum architecto necessitatibus pariatur est ipsum eveniet quibusdam labore neque ratione! Commodi voluptatibus doloremque asperiores maxime, cupiditate voluptas iusto, voluptatum autem, excepturi dolore veritatis quas tempore earum ipsum fugit! Impedit ipsum nam vitae ipsa aliquam, et exercitationem suscipit dolores ab ipsam maxime in, tenetur sit alias dolorum hic libero! Id aliquid, magnam nihil in natus facere? Dignissimos qui unde, sapiente molestiae et perspiciatis, est aliquid porro repellendus explicabo libero reprehenderit quas corporis rerum minus quisquam iusto culpa ex ipsa. Eveniet molestiae, ea alias ratione veniam dolorum libero fuga autem et quod earum tempora aperiam officiis sequi incidunt excepturi, facilis voluptas amet neque recusandae corrupti nostrum tenetur placeat suscipit. Iure, ut distinctio! Consequatur culpa doloribus iste repellat sit saepe porro consectetur corrupti dolore? Nulla dolores amet provident accusamus ipsum quaerat, saepe omnis architecto eveniet quae ab consectetur, quidem mollitia. Ea nesciunt, tempore libero illum voluptas ut odit veritatis neque nemo corporis, sapiente ex voluptates! Blanditiis dolores deserunt quaerat quisquam iure vero fuga illum unde aliquid. Enim doloremque illum deserunt molestiae quisquam, beatae expedita suscipit totam cumque modi maxime nisi eveniet necessitatibus autem rerum repellat iure. Delectus animi accusamus quisquam, quis amet laboriosam nostrum, sapiente error placeat beatae perspiciatis, autem inventore in velit tenetur omnis expedita porro non rem neque! Debitis deleniti eos quos ratione veniam repellendus fugiat vel, repudiandae cumque repellat quae recusandae rem assumenda est vero sed labore dolorem optio libero quibusdam at sint accusantium quam voluptatem. Quasi doloribus mollitia sequi laborum ea dolorem cum quibusdam tempora fugit modi alias tenetur ullam veritatis sed odit totam beatae magni, eveniet nihil quas iure a ratione eum consectetur? Laborum fuga recusandae voluptatibus, culpa tempore eos, voluptatum eligendi minus maxime velit, alias ratione quis itaque voluptates? Enim quibusdam eum animi consequatur corrupti assumenda quis? Nemo, qui quibusdam. Eum, sequi cumque! Perspiciatis eius suscipit accusantium sint cum. Accusantium suscipit atque maiores ducimus impedit, qui quod recusandae reiciendis, cupiditate voluptatum eos illo quidem labore. Tempora et quas quod architecto beatae? Doloribus asperiores assumenda illo odit minima recusandae ipsam ut labore odio alias officiis omnis expedita tempora quibusdam magnam eligendi quasi aut aliquid fuga dolorum molestias quo, praesentium soluta. Officia beatae mollitia recusandae quasi enim possimus non a dignissimos voluptatem ipsa. Suscipit dicta nam quam ratione deserunt provident? Unde magnam error asperiores voluptas molestias esse minima fugit dicta eum sequi adipisci corrupti, quod libero tenetur commodi eos modi voluptatibus deserunt minus repellat numquam velit nam incidunt accusantium. Quasi sunt laborum ratione quidem ex vitae aliquam assumenda ipsum esse aspernatur optio eligendi cum perspiciatis magnam molestias a iusto porro reprehenderit, quam libero laboriosam consequatur! Autem architecto, dolorem dolores earum rem voluptates vel cumque natus quo incidunt sint culpa quibusdam dolore esse! Perferendis quidem nam, deserunt dolor dolorum eos exercitationem quod iusto error fuga. In culpa vero, maxime, quae harum quia necessitatibus qui fugit natus assumenda similique ipsa! Dolor reprehenderit accusantium laboriosam ipsa, doloribus a eveniet iusto quibusdam placeat amet dolores deleniti expedita illum consequatur hic consequuntur in obcaecati neque eius dignissimos cupiditate ab. Excepturi, quod labore est voluptatibus atque nostrum, cupiditate necessitatibus deserunt rem eius incidunt soluta consequuntur repellendus autem? Quasi enim suscipit exercitationem praesentium autem. Ipsa tenetur cupiditate dolorem deserunt harum blanditiis praesentium fuga veniam placeat exercitationem. Delectus quibusdam doloribus sequi quae debitis nobis ad, consequatur ipsum placeat obcaecati odio repellat possimus eos ratione laudantium. Velit incidunt molestias id dolorum sapiente totam deleniti quis minus assumenda sunt, distinctio quas cum nostrum iste ducimus ab praesentium in! Veritatis earum esse accusamus aliquam, debitis placeat exercitationem architecto consequatur dolore quos totam voluptate fuga inventore praesentium at sequi impedit. Ipsum hic culpa voluptas fugit temporibus vel quod, corporis assumenda. Pariatur nostrum nam quae aut debitis laboriosam voluptatibus hic, quibusdam dolorem, maxime officia aperiam soluta deserunt quia vero voluptatem vitae quasi tempora ipsam veniam! Corrupti accusamus enim molestias temporibus cumque repudiandae minima quam in voluptatum? Incidunt sunt maiores soluta repudiandae voluptate rem possimus similique natus, minus iusto, beatae blanditiis provident ab nihil, temporibus quos! A quae soluta labore voluptatem minima nemo blanditiis, eligendi quis laudantium deserunt numquam. Quibusdam ut facilis eaque. Harum doloribus ab necessitatibus quo neque eum quia ea incidunt expedita, cumque est nulla ducimus in? Error totam delectus adipisci laborum quaerat maiores tempora ad cum esse, porro ex animi nesciunt id. Rerum enim nam soluta nesciunt odit quis, incidunt maiores reprehenderit nisi dicta iure, quos minima facilis, optio totam magnam dignissimos illo culpa dolores exercitationem? Error quaerat, maxime fuga at perspiciatis ea ullam sit minus aperiam facilis! Enim temporibus illum molestiae fugiat officia, sit at delectus facilis autem, excepturi dolore consequatur nostrum quod iusto dicta iure quisquam aut molestias! Voluptate natus facere magni possimus doloribus laudantium necessitatibus, explicabo maxime. Provident, animi temporibus repellat architecto quos id aliquid qui debitis dolore ipsam libero officiis cumque voluptatibus! Quos veritatis molestiae repellat eligendi tempora, molestias error veniam id dignissimos a suscipit velit rem harum maiores, necessitatibus iste voluptatem mollitia quod neque officiis. Rerum tempore fugit facere veritatis sapiente ducimus, harum enim culpa fuga officiis nemo pariatur natus quos voluptas rem omnis doloremque, numquam officia reprehenderit saepe esse quas soluta, totam perferendis. Maiores, nostrum nihil. Aliquam iure reiciendis sit asperiores consequatur rerum esse in corrupti, necessitatibus doloribus distinctio quidem officia facere modi consectetur fugiat facilis ex! Temporibus fuga in qui deserunt nisi praesentium officia sunt earum reiciendis harum nulla recusandae animi dolorum, alias aliquam nesciunt distinctio minima assumenda odio sequi enim neque saepe velit! Ipsum sint, ad aperiam minima saepe quidem eveniet illum sunt quam repellendus accusantium, libero nobis ratione recusandae natus cupiditate quas tempore dolor iusto aliquam adipisci ab hic nihil? Voluptatum aspernatur quas, saepe aliquid ab eum et voluptates omnis maxime sapiente assumenda ex sint inventore cumque eaque, iure non illo esse? Numquam incidunt aut earum deserunt laboriosam assumenda cupiditate illo sapiente delectus qui consequuntur hic quis, possimus voluptates, perferendis sunt distinctio, impedit fugit quae maxime molestias neque reprehenderit aliquid. Nisi, minus? Ab nulla culpa voluptas ut iusto repellendus, dolore et delectus laboriosam, quis similique non tempora. Sequi molestiae aut nostrum facilis hic, neque voluptates qui cupiditate accusamus dolore totam corrupti dignissimos sit veniam obcaecati. Temporibus possimus nesciunt neque illo fuga, tenetur dignissimos ratione eaque culpa dolorum doloribus facere sint suscipit voluptatem sapiente sequi ullam asperiores officia libero numquam deleniti provident maxime autem. Sunt assumenda voluptates ab eaque dolores iusto quasi quos nostrum asperiores debitis, ad a, voluptas vero? Fugiat consequuntur beatae, numquam reprehenderit adipisci quos laudantium velit temporibus delectus tenetur qui, illo mollitia vitae praesentium vero provident fugit dolor perferendis ab nihil asperiores. Fuga doloribus molestiae doloremque explicabo assumenda odio numquam fugit eveniet, facilis esse beatae quae voluptatem hic non dignissimos ex ducimus accusamus rem quas consectetur aliquid. Architecto recusandae minus ut velit, itaque quia sunt unde debitis reiciendis nostrum. Voluptatem perferendis, earum quidem libero quis corporis consequuntur consectetur temporibus provident rem odio quas nulla illo velit, quos aut eum minima saepe laboriosam quam. In quia quod iste, quidem asperiores reiciendis dolorum ullam saepe eum nostrum, hic dolorem. Quo odio at magnam, voluptas hic mollitia voluptates eos, consequuntur tempore praesentium sint numquam minima possimus est distinctio molestias esse iusto animi ipsam nostrum illum quia assumenda. Beatae necessitatibus cupiditate voluptas sed perferendis nesciunt neque ratione laudantium illo eius quas a, reprehenderit optio reiciendis eveniet alias hic accusamus maxime ipsam dicta itaque suscipit. Fugit hic eos impedit aliquid et asperiores inventore porro provident ducimus rem sunt numquam tenetur dignissimos esse cum, saepe mollitia? Necessitatibus error quisquam deleniti qui alias! Nisi, ab, recusandae perspiciatis possimus nam temporibus eaque sapiente cum quos repudiandae deserunt corrupti, dolorum soluta porro dolore consequuntur aut aliquid iusto a! Ipsum laboriosam distinctio fuga eaque recusandae, dolorum aperiam quod facilis cumque ea debitis? Enim maxime voluptatibus, at ut earum itaque nobis a incidunt, pariatur animi eos harum! Repellendus eum ullam impedit reprehenderit itaque consequuntur, aliquam quaerat beatae. Corporis labore excepturi repudiandae fugit odio quasi nam dolores dolore illo reiciendis veritatis eos deserunt sed exercitationem reprehenderit beatae ea aut iusto, enim eum distinctio deleniti facere consectetur. Aperiam repellendus veritatis magnam vero amet rem itaque odit adipisci praesentium accusantium nostrum numquam placeat tempora rerum illo nam modi, inventore veniam ipsam quasi laborum sint! Ea incidunt culpa excepturi repudiandae maiores! Maiores dolore tempora delectus, ipsa perspiciatis atque possimus deserunt doloremque sapiente nisi itaque alias aliquam placeat corrupti laborum facere, exercitationem ut assumenda, ex eos nihil! Ad tempora id modi repellat excepturi eum dolor architecto magnam, fuga ex ducimus deleniti iusto nostrum quod possimus nisi distinctio minus saepe nobis consequatur quibusdam atque molestiae? Commodi reprehenderit, accusamus incidunt iusto consequuntur quibusdam eos? Ullam ipsa, quae perferendis quod delectus tempore! Mollitia ut, maxime cumque architecto eaque fugiat dolorum soluta nesciunt inventore esse tempora tenetur similique? Nesciunt commodi sapiente eveniet id quisquam libero perspiciatis ex veniam cum aliquam perferendis, fugiat voluptatum ad illo in non. Est eum a doloremque modi quas sed, obcaecati excepturi culpa odio commodi harum iure accusamus animi praesentium illo enim. A laudantium obcaecati tempora aliquid numquam asperiores? Officia, deleniti commodi. Quisquam modi, nesciunt quis rerum corrupti possimus consectetur. Illum hic optio dignissimos tempora non aspernatur, nulla amet quasi inventore voluptatibus! Similique esse expedita, dolores nulla itaque dolorum? Fuga asperiores est provident ratione? Ex, repudiandae. Fugiat perspiciatis quis sequi dolore atque veritatis asperiores sed, commodi molestiae temporibus velit expedita maxime sunt eligendi nemo, explicabo veniam! Iusto, quidem eum dignissimos reiciendis exercitationem repellat ipsum, corrupti laudantium cum sed quos aspernatur, quibusdam assumenda sequi vel. Consequatur repudiandae ad inventore in facilis temporibus voluptates aspernatur ratione debitis ipsa doloremque repellat non quas quibusdam eos ipsam earum architecto quidem atque, cumque deleniti quia. Illum, pariatur dolore! Quam architecto, quaerat mollitia error quibusdam doloribus voluptates? Cupiditate, officia. Quibusdam ipsum non minus praesentium in, incidunt minima nam ullam voluptates aliquam voluptatum sequi maxime autem ut illum ratione accusamus. Impedit facere sit nostrum rem. Recusandae officiis in quasi provident pariatur reprehenderit similique eligendi voluptates, et odit quia laboriosam eos cumque fugit numquam consequuntur incidunt nisi porro. Dolores fugit perspiciatis iste voluptates debitis molestiae. Sapiente excepturi hic quo nobis totam, omnis blanditiis? Exercitationem a ut ipsa sit molestias expedita doloribus excepturi at totam aliquid placeat laborum hic laboriosam iste nobis, suscipit, atque voluptatum officia incidunt ipsum? Autem, quo sint unde asperiores assumenda ipsa libero? Similique nesciunt eveniet delectus ad voluptate recusandae qui quis corrupti at nam. Aperiam earum vel provident et facere molestiae porro ipsam facilis, libero ullam sapiente, veritatis est reiciendis ducimus nemo. Harum consequuntur praesentium vel culpa nisi sit! Minus nulla, excepturi at non quod aliquam.</p>\n</body>\n</html>",
    "created": "2025-11-09T13:25:08.354785"
  }
];

// Function to load preloaded codes into localStorage
function loadPreloadedCodes() {
    const STORAGE_KEY = "pastebin_codes";
    
    // Always load preloaded codes (overwrite on each page load)
    // This ensures the static site always has the latest files
    localStorage.setItem(STORAGE_KEY, JSON.stringify(PRELOADED_CODES));
    
    console.log(`Loaded ${PRELOADED_CODES.length} preloaded code files`);
}

// Auto-load on page load
if (typeof window !== "undefined") {
    window.addEventListener("DOMContentLoaded", loadPreloadedCodes);
}
