def facto(n):
    if(n==0 or n==1):
        return 1
    return n*facto(n-1)
n=int(input("Enter a number:"))
print(f"The factorial of this number is : {facto(n)}")

