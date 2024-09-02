'''
Core module for randomization takes size of die and number of rolls to return an array of generated rolls
Returns [0] if input error
'''
import time as t
import random as r

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

if __name__ == "__main__":
    print(roll(input("How many sides?"),input("How many times?")))