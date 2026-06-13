import re

def jaccard(line_a :str, line_b: str) :  #-> float
    clear_a = re.sub(r'[^\w\s]','',line_a.lower()) 
    clear_b = re.sub(r'[^\w\s]','',line_b.lower()) 
    
    set_a = set(clear_a.split())
    set_b = set(clear_b.split())  
    
    if not set_a or not set_b:
        return 0
    
    shared = set_a & set_b         #pick the common from both the sets
    all = set_a | set_b             #picks everything from both the sets
    
    return len(shared) / len(all)