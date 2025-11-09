'''
s=1
w=-1
g=0
'''
comp = -1  # Let's say -1 represents "Water"
you_input = input("Enter your attack mode (Snake/Water/Gun): ")

# Define the choices
youD = {"Snake": 1, "Water": -1, "Gun": 0}

# Check if user input is valid
if you_input not in youD:
    print("Invalid input. Please choose from Snake, Water, or Gun.")
else:
    you = youD[you_input]

    if comp == you:
        print("The game is a draw.")
    elif (comp == -1 and you == 1) or (comp == 0 and you == -1) or (comp == 1 and you == 0):
        print("You win!")
    else:
        print("You lose!")
