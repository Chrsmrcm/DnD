from func.functions import *

'''
main combat loop of program. runs through combat dictionary and prompts for various choices
can also save the combat as json file for later
'''
def run_combat(combat_dict: dict):
    
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
        report(player,combat_dict)
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
                targets = input("What are the target names? (Enter multiple values separated by commas or leave blank for ALL):")
                amount = input("Enter damage (negative values will heal): ")
                damage(targets,amount,combat_dict)
            elif choice == "4":
                remove(player,combat_dict)                
                #special cases all characters on hold or all removed
                if len(initiative) < 1:
                    if len(hold) > 0:
                        initiative.append(hold.pop(0))
                    else:
                        print("Initiative is empty")
                        keep_going = False                        
                turn = False
            #enter undo mode pop past to reset initiative, combat_dict and hold
            elif choice == "5":
                try:                    
                    undo_mode = True
                    player,combat_dict,initiative,hold = past.pop(0)
                    initiative.insert(0,player)
                    turn = False
                except IndexError:
                    print("Undo queue is empty") 
            #add players
            elif choice == "6":
                print("New additions will be placed in hold queue.")
                gather_initiatives(combat_dict,True,hold)
                print(f"Hold: {hold}\n")
            #full player printout
            elif choice == "7":
                report(player,combat_dict)
                for key in combat_dict.keys():
                    report(key,combat_dict)
            #quit
            elif choice == "8":
                answer = input("Would you like to save? Y or N: ")
                if answer.upper() == "Y":
                    save(combat_dict)
                keep_going, turn = False, False
            else:
                initiative.append(player)
                turn = False
                
            if choice != "5":
                undo_mode = False