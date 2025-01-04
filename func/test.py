#check if number 1 - 20 is prime
target = 4
found = False
for number in range(2,target):
    #target % number
    #if remainder then false
    if target % number == 0:
        print("false!")
        found = True
        
if not found:        
    print ("true!")
        
