import json as j
import random as r
import sys as s
import time as t
import copy as c
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
        for _ in range(times):
            output.append(r.randrange(1,sides+1))
        
        return output
    else:
        return [0]        
        
'''
pulls in premade combat units from a json file
'''
def load_premade(combat_dict: dict):
    r.seed(t.time())
    file_name = input("What is the name of the file? ")
    path = Path.cwd() / "data" / file_name
    with open(path, 'r') as file:
        data = j.load(file)    
    
    #seed combat dictionary w preloads
    for key in data.keys():        
        combat_dict[key] = [int(data[key]["initiative"])+roll(20,1)[0],int(data[key]["hp"]),data[key]["notes"],int(data[key]["initiative"])]
        
    print(f"Loaded {len(data.keys())} characters...")    


'''
runs a user input loop for ad hoc character entry
'''
def gather_initiatives(combat_dict: dict,in_prog: bool=False,hold: list=[]):    
    
    keep_going = "Y"
    while keep_going.upper() == "Y":
        #start gathering inits
        name = input("Input character name: ")
        i_mod = input("Input initiative modifier: ")
        hp = input("Input hit points: ")
        notes = input("Input notes: ")
        
        #a little error checking
        try:
            init = int(i_mod) + roll(20,1)[0]
        except ValueError:
            print("Problem converting initiative to number, default 0 entered")
            init = 0
        try:
            hp = int(hp)
        except ValueError:
            print("Problem converting hit points to number, default 0 entered")
            hp = 0
        
        #check for name colision
        while name in combat_dict:
            name = input("That character exists. Input new name: ")
            
        combat_dict[name] = [init,hp,notes,i_mod]
        if in_prog:
            hold.append(name)
        keep_going = input("Enter more? Y or N: ")
'''
prints the menu of player choices for turns
'''
def print_menu():
    print("\n1) Hold turn")
    print("2) Change note")
    print("3) Log damage")
    print("4) Remove character")    
    print("5) Undo")
    print("6) Add Players")
    print("7) Full Report")
    print("8) Quit")
    print("Press ENTER to pass turn\n")

'''
changes from key:[val,ues] to key:{val:u,e:s} for easier storage/retrieval
'''
def format_dict(combat_dict: dict) -> dict:#change this to save modifiers
    new = {}
    for key in combat_dict:
        new[key] = {"initiative":combat_dict[key][3],
                    "hp":combat_dict[key][1],
                    "notes":combat_dict[key][2]}
    return new
    
'''
saves the current combat dictionary as a json file in data
'''   
def save(combat_dict: dict):
    file_name = input("What would you like to call the file? ") + ".json"
    path = Path.cwd() / "data" / file_name
    
    new = format_dict(combat_dict)
    
    with open(path, "w") as outfile: 
        j.dump(new, outfile)

'''
logs damage to the combat dict to each player in the list of targets
if the list of targets is empty, it assigns the listed damage to ALL
'''
def damage(targets: str,amount: int,combat_dict: dict):
    try:
        amount = int(amount)
    except ValueError:
        print("Error with amount, must be int, operation aborted")
        return 0
    
    try:
        if targets:
            for target in targets.split(','):
                try:
                    combat_dict[target][1] -= amount
                    print(f"{target} is now at {combat_dict[target][1]} hitpoints")
                except KeyError:
                    print(f"{target} not found.  No change made.")
        else:
            for target in combat_dict.keys():
                combat_dict[target][1] -= amount
                print(f"{target} is now at {combat_dict[target][1]} hitpoints")
    except:
        print("Error in damage assignment to list")
        
'''
removes a player from the combat dictionary
'''
def remove(player: str,combat_dict: dict):
    del(combat_dict[player])
    print(f"{player} has been removed.")

'''
prints out a given character, their hp, and any notes
'''  
def report(player: str,combat_dict: dict):
    print(f"{player}:\n HP: {combat_dict[player][1]}\n Notes: {combat_dict[player][2]}\n")