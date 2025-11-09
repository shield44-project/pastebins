import random

no = random.randint(1, 100)
tries = 0

guess = int(input("Enter your guess: "))
tries += 1

while guess != no:
    if guess > no:
        print("Your guess is higher than the number.")
    else:
        print("Your guess is lower than the number.")
    guess = int(input("Try again: "))
    tries += 1

print(f"You guessed it correct! The number is {no}.")
print(f"It took you {tries} tries.")

