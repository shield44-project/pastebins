x=1212

temp=x
digits=0

while temp>0:
	digits+=1
	temp//=10

first_half=0
second_half=0

temp=x
for i in range(digits//2):
	second_half+=temp%10
	temp//=10


while temp>0:
	first_half+=temp%10
	temp//=10

print(first_half == second_half)
