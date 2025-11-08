n=int(input("num:"))
rev=0
orig=n
while n!=0:
	digit=n%10
	rev=rev*10+digit
	n=n//10
print(rev)
