weight=float(input("Enter your weight in kg:"))
height=float(input("Enter your length in metre:"))
bmi=weight/height**2

print(f"Your BMI is ",bmi)

if bmi<18.5:
	print("You are underweight")
elif bmi>=18.5 and bmi<=24.9:
	print("You are normal weight")
elif bmi>=25 and bmi<=29.9:
	print("You're overweight")
else:
	print("You are obese")



