n=1245
rev_n=0
while n!=0:
	digit=n%10
	rev_n=digit*10+rev_n
	n//=10
print(rev_n)
