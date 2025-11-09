sequence = [4, None, 6, 9, 0, None, None, 65, 90]

print("Original Sequence:", sequence)

# Fill missing values (replace None with 0)
for i in range(len(sequence)):
    if sequence[i] is None:
        sequence[i] = 0
print("After Filling Missing Values:", sequence)

# Remove a number (remove element at index 2)
removed = sequence.pop(2)
print("After Removing Element at index 2 (removed:", removed, "):", sequence)

# Add a new number (e.g., 45)
sequence.append(45)
print("After Adding Element 45:", sequence)

print("Modified Sequence:", sequence)

