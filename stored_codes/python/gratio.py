n=int(input("Enter a number:"))
fiblist=[0,1]
for i in range(0,n):
	fiblist.append(fiblist[i]+fiblist[i+1])
print(fiblist)
gratio=[fiblist[i]/float(fiblist[i-1]) for i in range(2,len(fiblist)) ]
print(gratio)
