from func.functions import *

combat_dict = {}

file = input("Would you like to load from file? Y or N: ")
live = input("Would you like to enter info? Y or N: ")

#load sequence
if file.upper() == 'Y':
    load_premade(combat_dict) 

if live.upper() == 'Y':
    gather_initiatives(combat_dict)

#start the combat loop
run_combat(combat_dict)