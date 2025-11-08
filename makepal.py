n=int(input("Enter a number:"))
'''
t=n
count=0
while t>0:
	count+=1
	t//=10
temp=n
rev=0
#check if palindromes
while temp>rev:
	rev=rev*10+temp%10
	temp//=10
if temp==rev or temp==rev//10:
	print("Already {} is palindrome".format(n))
else:
	temp=n
	rev=0
	while temp>0:
		rev=rev*10+temp%10
		temp//=10
	make_pal=rev+n

	rev_make_pal=rev_make
	while make_pal!=rev_make_pal:
'''
 
