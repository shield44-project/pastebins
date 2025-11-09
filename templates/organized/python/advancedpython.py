####WALRUS
# if (n := len([1, 2, 3, 4, 5])) > 3:
#         print(f"List is too long ({n} elements, expected <= 3)")

# age: int=233
# def whatisthis(name: str) -> str:
#     return f"Hello {name}"
# print(whatisthis("Yashas"))
# def sum(a: int,b: int) -> int:
#     return a+b
# print(sum(3,5))
from typing import List, Tuple, Dict, Union
# List of integers
numbers: List[int] = [1, 2, 3, 4, 5]
# Tuple of a string and an integer
person: Tuple[str, int] = ("Alice", 30)
# Dictionary with string keys and integer values
scores: Dict[str, int] = {"Alice": 90, "Bob": 85}
# Union type for variables that can hold multiple types
identifier: Union[int, str] = "ID123"
identifier = 12345 # Also valid


# #####MATCH CASE#########
# def http_status(status):
#     match status:
#         case 200:
#             return "OK"
#         case 404:
#             return "Not Found"
#         case 500:
#             return "Internal Server Error"
#         case _:
#             return "Unknown status"
# print(http_status(200))
# dict1={"a":1,"b":2}
# dict2={"c":3,"d":4}
# merged= dict1 | dict2
# print(merged)
# with (
# open('file1.txt') as f1,
# open('file2.txt') as f2
# ):
# Process files
# try:
#     a=int(input("Enter the number:"))
# except Exception as e:
#       print(e)

# L={1,2,3,4,5,6,7,8}
# for i,item in enumerate(L):
#     if i==2 or i==4 or i==6:
#         print(item)
# def sq(n):
#     return n*n
# sq=lambda x:x*x 
# bq= lambda a,b,c:a+b+c
# print(sq(2))
# print(bq(3,4,5))
a=["a","pp","le"]
jointhem="".join(a) # "put anything here they will join the list elements"
print(jointhem)
l="{1} is a good {0}".format("Harry","boy")
print(l)
L=[1,2,3,4,5,6,7,8]
sw=lambda x:x*x*x
swlist=map(sw,L)
print(list(swlist))
#filter
def odd(n):
    if(n%2!=0):
        return True
    return False
l=filter(odd,L)
print(list(l))
# reduce
def sum(a,b):
    return a+b
from functools import reduce
mul=lambda x,y:x*y
print(reduce(mul,L))
print(reduce(sum,L))

