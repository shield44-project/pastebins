# n=int(input("Enter the number:"))
# v=0
# for i in range(1,n+1):
#     v+=i

# print(v)

# n=int(input("Enter the number:"))
# p=1
# for m in range(1,n+1):
#     p=p*m
# print(p)
# n=int(input("Enter the number:"))
# v=0
# for i in range(1,n+1):
#     v+=i/2
# print(v)
# n=int(input("Enter the number:"))
# for i in range(2,n):
#    if(n%i==0):
#        print("The number is not prime")
#        break
# else:
#        print("The number is prime")
# n=int(input("Enter the number:"))
# i=1
# for i in range(1,n+1):
#     print(" "*(n-1), end="")
#     print("")
#     print("*"*(i), end="")
# print("")

# n = int(input("Enter the number: "))
# for i in range(1, n+1): 
#     if(i==1 or i==n):
#         print("*"* n, end="")
#     else:
#         print("*", end="")
#         print(" "* (n-2), end="")
#         print("*", end="")
#     print("")
# n = int(input("Enter the number: "))
# for i in range(1,11):
#     print(f"{n}X{11-i}={n*(11-i)}")
# n=int(input("Enter the number:"))
# for i in range(1,n+1):
#     print(" "*(n-i), end="")
#     print("*"*(2*i-1), end="")
#     print("")
# a=int(input("Enter a number:"))
# b=int(input("Enter a number:"))
# c=int(input("Enter a number:"))
# if(a>b and a>c):
#         print(f"{a} is the greatest number")
# elif(b>a and b>c):
#         print(f"{b} is the greatest number")
# else:
#         print(f"{c} is the greatest number")
# def use(a,b,c):
#     if(a>b and a>c):
#         return a
#     if(b>a and b>c):
#         return b
#     if(c>a and c>b):
#         return c
# a=int(input("Enter a number:"))
# b=int(input("Enter a number:"))
# c=int(input("Enter a number:"))
# print(use(a,b,c))
# c=int(input("Enter a number:"))
# def ctof():
#     return 9/5*(c)+32
# print(f"{round(ctof(),4)}°F")
# f=int(input("Enter a number:"))
# def ftoc():
#     return (5*(f-32))/9
# print(f"{round(ftoc(),2)}°C")
# def f_to_c(f):
#     return 5*(f-32)/9

# f = int(input("Enter temperature in F: "))
# c = f_to_c(f)
# print(f"{round(c, 2)}°C")
# i=   int(input("Enter a number:"))       
# def fa(n):
#     if(n==1 or n==0):
#         return 1
#     else:
#             return n*fa(n-1)
# print(fa(i)) 
# number=int(input("Enter a number:"))
# def sum_of_n_natural_numbers(n):
#        if(n==1): 
# def pattern(n):
#     if(n==0):
#         return
#     print("*" * n)
#     pattern(n-1)


# pattern(3)
# inch=int(input("Enter the number:"))
# def intocm(inch):
#     return inch*2.54
# print(intocm(4))
# def pattern(n):
#      if(n==0):
#           return
#      else:
#           print("*"*n)
#           pattern(n-1)

# pattern(3)
# def rem(l,word):
#     n=[]
#     for item in l:
#         if not(item==word):
#             n.append(item.strip(word))
#         return n
# l = ["Harry", "Rohan", "Shubham", "an"]
# print(rem(l, "an"))
# def mult(n):
#     for i in range(1,11):
#         print(f"{n}X{i}={n*i}")
     
# mult(3)