import time as t
import random as r
import json
from pathlib import Path

'''
Core module for randomization takes size of die and number of rolls to return an array of generated rolls
Returns [0] if input error
'''
def roll(sides: int,times:int) -> list[int]:
    
    try:
        sides, times = int(sides),int(times)
    except:
        return [0]
    
    if sides > 0 and times > 0:
        output = []
        r.seed(t.time())
        for _ in range(times):
            output.append(r.randrange(1,sides+1))
        
        return output
    else:
        return [0]        

'''
pulls in premade combat units from a json file
'''
def load_premade(combat_dict: dict):
    file_name = input("What is the name of the file? ")
    path = Path.cwd() / "data" / file_name
    with open(path, 'r') as file:
        data = json.load(file)    
    
    #seed combat dictionary w preloads
    for key in data.keys():        
        combat_dict[key] = [int(data[key]["initiative"]),data[key]["notes"]]
        
'''
runs a user input loop for ad hoc character entry
'''
def gather_initiatives(combat_dict: dict):
    keep_going = "Y"
    while keep_going.upper() == "Y":
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
        keep_going = input("Enter more? Y or N: ")
        
'''
main combat loop of program. runs through combat dictionary and prompts for various choices
can also save the combat as json file for later
'''
def run_combat(combat_dict: dict):
    pass
    
if __name__ == "__main__":
    print(roll(input("How many sides?"),input("How many times?")))