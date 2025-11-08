import cmath

num=eval(input("Enter the value(note j is the imag part used):"))

print("The sqaure root of {0} is {1:0.3f}+{2:0.3f}j".format(num,cmath.sqrt(num).real,cmath.sqrt(num).imag))
