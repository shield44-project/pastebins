n=42123
if n==0 or (n%10==0 and n!=0):
	print(False)
elif n<0:
	print(False)
else:
	rev=0
	temp=n
	while temp>rev:
		rev=rev*10+temp%10
		temp//=10
	print(temp==rev or temp==rev//10)
