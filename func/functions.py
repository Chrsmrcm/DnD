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
        combat_dict[key] = [int(data[key]["initiative"])+roll(20,1)[0],int(data[key]["hp"]),data[key]["notes"]]
    print(f"Loaded {len(data.keys())} characters...")    
'''
runs a user input loop for ad hoc character entry
'''
def gather_initiatives(combat_dict: dict):
    keep_going = "Y"
    while keep_going.upper() == "Y":
        #start gathering inits
        name = input("Input character name: ")
        init = input("Input initiative modifier: ")
        hp = input("Input hit points: ")
        notes = input("Input notes: ")
        
        #a little error checking
        try:
            init = int(init) + roll(20,1)[0]
        except ValueError:
            print("Problem converting initiative to number, default 0 entered")
            init = 0
        try:
            init = int(hp)
        except ValueError:
            print("Problem converting hit points to number, default 0 entered")
            hp = 0
        
        #check for name colision
        while name in combat_dict:
            name = input("That character exists. Input new name: ")
            
        combat_dict[name] = [init,hp,notes]
        keep_going = input("Enter more? Y or N: ")
'''
prints the menu of player choices for turns
'''
def print_menu():
    print("\n1) Hold turn")
    print("2) Change note")
    print("3) Log damage")
    print("4) Remove character")
    print("5) Quit")
    print("Press ENTER to pass turn\n")

'''
saves the current combat dictionary as a json file in data
'''   
def save(combat_dict: dict):
    file_name = input("What would you like to call the file? ") + ".json"
    path = Path.cwd() / "data" / file_name
    with open(path, "w") as outfile: 
        json.dump(combat_dict, outfile)
'''
main combat loop of program. runs through combat dictionary and prompts for various choices
can also save the combat as json file for later
'''
def run_combat(combat_dict: dict):
    #build initiative list by grabbing max value[0] and iterate up the list pushing names onto initiative
    initiative = sorted(combat_dict, key=combat_dict.get)
    hold = [] 
    
    keep_going = True
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
            choice = input("What would you like to do: ")
            if choice == "1" and len(initiative) > 0:
                hold.append(player)
                turn = False
            elif choice == "2":
                combat_dict[player][2] = input("Add new note: ")
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
                print(f"{player} has been removed.")
                turn = False
                #special case where all characters on hold and current character is removed
                if len(initiative) < 1:
                    initiative.append(hold.pop(0))
            elif choice == "5":
                answer = input("Would you like to save? Y or N: ")
                if answer.upper() == "Y":
                    save(combat_dict)
                keep_going, turn = False, False
            else:
                initiative.append(player)
                turn = False
            print()
if __name__ == "__main__":
    
    combat_dict = {"alan":[20,40,"i'm a pretty pony"],"steve":[30,40,"beep"],"Rachel2.0":[18,40,"poisoned af"],"Lori":[999,40,"BEES!"]}
    run_combat(combat_dict)