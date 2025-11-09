n=int(input("Enter a number:"))
maxprim=-1

while n%2==0:
	maxprim=n
	n=n/2

for i in range(3,int(n**(0.5))+1,2):
	while n%i==0:
		maxprim=i
		n=n/i
	if n>2:	
		maxprim=n
print(maxprim)
