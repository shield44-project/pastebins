#389=3^3+8^3+9^3 is called armstrong number(if)
#xyz=x^n+y^n+z^n armstrong number of order n
"""
9981%10=1
998%10=8
99%10=9
9%10=9"""
n=153
sum=0
copy=n
order=len(str(n))
while(n>0):
	digit=n%10
	sum+=digit**order
	n=n//10 # 8891 ko 889 so floor division whener number >0 it works
if sum==copy:
	print("Armstrong number of order ",order)
else:
	print("Not a armstrong number")
