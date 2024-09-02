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
def load_premade(combat_dict: dict) -> dict:
    file_name = input("What is the name of the file? ")
    path = Path.cwd() / "data" / file_name
    with open(path, 'r') as file:
        data = json.load(file)    
    
    #seed combat dictionary w preloads
    for key in data.keys():        
        combat_dict[key] = [int(data[key]["initiative"]),data[key]["notes"]]
    
    return(combat_dict)
    
if __name__ == "__main__":
    print(roll(input("How many sides?"),input("How many times?")))