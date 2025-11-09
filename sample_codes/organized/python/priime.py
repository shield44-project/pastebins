n=int(input("Enter a number:"))

for i in range(1,n):
    if(n%i) ==0:
        print("The number is not prime")
    break
else:
    print("The number is prime")

    print("End of program")