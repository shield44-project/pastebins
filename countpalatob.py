A=int(input("Enter a number:"))
B=int(input("Enter another number:"))

for i in range(A,B+1):
	rev=0
	temp=i
	while temp>rev:
		rev=rev*10+temp%10
		temp//=10
	if rev==temp or rev//10==temp and (i%10!=0):
		print(i)
