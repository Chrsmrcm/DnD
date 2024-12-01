import json as j
import random as r
import sys as s
import time as t
import threading as th
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
def gather_initiatives(combat_dict: dict):    
    r.seed(t.time())
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
    print("6) Quit")
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
main combat loop of program. runs through combat dictionary and prompts for various choices
can also save the combat as json file for later
'''
def run_combat(combat_dict: dict):
    #build initiative list by grabbing max value[0] and iterate up the list pushing names onto initiative
    initiative = sorted(combat_dict, key=combat_dict.get)
    hold = [] 
    
    keep_going = True
    undo_mode = False
    #variable that limits the number of undo actions
    past_max = 10
    #initialize undo queue
    past = []
    while keep_going:
        #check for characters on hold (if none pass)
        if hold:
            print("Currently these characters are holding their turns:")
            for i in range(len(hold)):
                print(f"{i}) {hold[i]}")
                
            answer = input("\nEnter a valid choice to take turn or press ENTER to pass to normal initiative: ")
            try:
                answer = int(answer)
                initiative.insert(0,hold.pop(answer))
            except:
                pass
        #display current turn
        player = initiative.pop(0)
        print("=======================Start Turn=============================")
        print(f"{player}:\n HP: {combat_dict[player][1]}\n Notes: {combat_dict[player][2]}\n")
        print(f"Lineup: {initiative}")
        print_menu()
        
        turn = True
        while turn:
            #log player,state if buffer not full and not currently undoing
            #if past is maxed, make room
            #if not undo mode, log activity
            if len(past)>past_max:
                past.pop(-1)
            if not undo_mode: 
                event = [player,c.deepcopy(combat_dict),c.deepcopy(initiative),c.deepcopy(hold)]
                past.insert(0,event)            
        
            choice = input("What would you like to do: ")
            if choice == "1" and len(initiative) > 0:
                hold.append(player)
                turn = False
            elif choice == "2":
                combat_dict[player][2] = input("Change note to: ")
            elif choice == "3":
                target = input("What is the target name? ")
                damage = input("Enter damage (negative values will heal): ")
                try:
                    damage = int(damage)
                except ValueError:
                    damage = 0
                try:
                    combat_dict[target][1] -= damage
                    print(f"{target} is now at {combat_dict[target][1]} hitpoints")
                except KeyError:
                    print("Target not found.  Check name and try again: ")
                    print(f"Lineup: {initiative}")
            elif choice == "4":
                del(combat_dict[player])
                print(f"{player} has been removed.")
                turn = False
                #special cases all characters on hold or all removed
                if len(initiative) < 1:
                    if len(hold) > 0:
                        initiative.append(hold.pop(0))
                    else:
                        print("Initiative is empty")
                        keep_going = False
            elif choice == "5":
                try:
                    #enter undo mode
                    undo_mode = True
                    #pop front of past stackm to reset initiative, combat_dict andh old queue
                    #event = past.pop(0)
                    player,combat_dict,initiative,hold = past.pop(0)
                    initiative.insert(0,player)
                    #end turn to reset
                    turn = False
                except IndexError:
                    print("Undo queue is empty")
                    
            elif choice == "6":
                answer = input("Would you like to save? Y or N: ")
                if answer.upper() == "Y":
                    save(combat_dict)
                keep_going, turn = False, False
            else:
                initiative.append(player)
                turn = False
                
            if choice != "5":
                undo_mode = False
            
            
            
if __name__ == "__main__":
    
    combat_dict = {"alan":[20,40,"i'm a pretty pony"],"steve":[30,40,"beep"],"Rachel2.0":[18,40,"poisoned af"],"Lori":[999,40,"BEES!"]}
    run_combat(combat_dict)