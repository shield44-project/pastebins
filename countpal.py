n=int(input("Enter N to get palindromes between 1 to N:"))
#rev=0 it is wrong as rev needs to reset for each number
count=0
pal_list=[]
for i in range(1,n+1):
	temp=i
	rev=0
	if temp==0 or (temp!=0 and temp%10==0):
		print("checking..")
	else:
		while temp>0:
			rev=rev*10+temp%10
			temp//=10
		if rev==i:
			count+=1
			pal_list.append(i)
		
print("Number of palindromes is",count)
print("Palindromes list is",pal_list)
