n=153
sum=0
temp=n
t=n
digits=0
while t>0:
	digits+=1
	t//=10
while temp>0:
	digit=temp%10
	sum=digit**digits+sum
	temp//=10
if sum==n:
	print("arm")
else:
	print("no arm")

