# Import what is needed
import os
import sys


# Obtain user input to a number
response = raw_input("Please enter a value(1-5): ")



#If statement to call the appropriate script
if response == "1":
    print("Pybot will begin moving forwards.\n")
    os.system('sudo python forward.py')
elif response == "2":
    print ("Pybot will begin moving backwards.\n")
    os.system('python backward.py')
elif response == "3":
    print ("Pybot will begin moving left.\n")
    os.system('sudo left.py')
elif response == "4":
    print ("Pybot will begin moving right.\n")
    os.system('python right.py')
elif response == "5":
    print ("Pybot will begin moving right.\n")
    os.system('python spin.py')
else:
    print ("Command not recognized.\n")
