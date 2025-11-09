A=[[1,2,5],[3,4,7],[5,6,9]]
B=[[1,3],[3,4],[7,6]]
C=[[0,0],[0,0],[0,0]]
for i in range(0,len(C)):
	for j in range(1,len(C[0])):
		for k in range(1,len(B)):
			C[i][j]+=A[i][k] * B[k][j]
for row in C:
	print(row)

