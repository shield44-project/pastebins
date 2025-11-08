n=int(input("Enter a number:"))
temp=n
binary=""
while temp>0:
	binary=str(temp%2)+binary
	temp//=2
print(binary)
if (binary==binary[::-1]):
	print("%d is a palindrome"%n)
else:
	print("%d is not a palindrome"%n)
