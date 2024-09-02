class Initiative:    
    
    def __init__(self):
        self.initiative = []
        
    def insert(self,score: int,name: str):
        
        self.initiative.append([score,name])
    
    def list_initiative(self):
        
        return self.initiative
        
    def order(self):
        
        self.initiative.sort(reverse=True)
        
        
if __name__ == "__main__":
    a = Initiative()
    a.insert(10,"sam")
    a.insert(9,"dave")
    a.insert(11,"sally")
    a.order()
    print(a.list_initiative())