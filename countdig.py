n=int(input("Enter a number:"))
count=0
while n!=0:
	digit=n%10
	n=n//10
	count+=1
print(count)
