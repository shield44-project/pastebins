sequence=[4,None,6,9,0,None,None,65,90]
print("Original Sequence:",sequence)
filled_seq=[]
for num in sequence:
	if num is None:
		filled_seq.append(0)
	else:
		filled_seq.append(num)
print("Sequence after replacing None with 0:", filled_seq)
print("Removed second index in sequence:",sequence.pop(2),sequence)
print("Added element 45 to the sequence:",sequence.append(45),sequence)
print("Modified Sequence:",sequence)

