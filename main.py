from func.functions import *

combat_dict = {}

file = input("Would you like to load from file? Y or N: ")
live = input("Would you like to enter info? Y or N: ")

#load loop
if file.upper() == 'Y':
    combat_dict = load_premade(combat_dict)
        
while live.upper() == 'Y':
    #start gathering inits
    name = input("Input character name: ")
    init = input("Input initiative: ")
    #a little error checking
    try:
        init = int(init)
    except ValueError:
        print("Problem converting initiative to number, default 0 entered")
        init = 0
    notes = input("Input notes: ")
    
    #check for name colision
    while name in combat_dict:
        name = input("That character exists. Input new name: ")
        
    combat_dict[name] = [int(init),notes]
    live = input("Enter more? Y or N: ")

print(combat_dict)
#start the combat loop

    