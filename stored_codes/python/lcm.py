a=int(input("Number1: "))
b=int(input("Number2: "))
# maxNum=max(a,b)
# while(True):
# 	if(maxNum%a==0 and maxNum%b==0):
# 		break
# 	maxNum=maxNum+1

# print(maxNum)

lcm=max(a,b)
while(True):
    if (lcm%a==0 and lcm%b==0):
        break
    lcm=lcm+1
print(lcm)
