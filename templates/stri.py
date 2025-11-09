str ="New Delhi is capital of India Bengaluru is capital of Karnataka"
wordCount=len(str.split())
print("Total Number of words : ", wordCount)#print the word count
counts = dict()# Create an empty dictionary
words = str.split()
for word in words:
	if word in counts:
		counts[word] =counts[word]+ 1
	else:
		counts[word] = 1
for key in list(counts.keys()):
	print(key, ":", counts[key])
searchWord=input("Enter the word to search : ")
result = str.find(searchWord)
if(result!=-1):#if Found disply success message
	print(searchWord +" Word found in string")
else:#if not Found disply unsuccessfull message
	print(searchWord + " !!!!! Word not found in string")
