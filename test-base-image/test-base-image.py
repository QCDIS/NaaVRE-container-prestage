import copy
import numpy as np
from collections import Counter




arr = np.array([1, 2, 3, 4, 5])

print(arr)

print(type(arr))

li1 = [1, 2, [3,5], 4]
  
  
li2 = copy.copy(li1) 
  
li3 = copy.deepcopy(li1) 



print(Counter(['B','B','A','B','C','A','B',
               'B','A','C']))
    
print(Counter({'A':3, 'B':5, 'C':2}))
    
print(Counter(A=3, B=5, C=2))
a = 2 + 1

import json
filename = "/tmp/a_" + id + ".json"
file_a = open(filename, "w")
file_a.write(json.dumps(a))
file_a.close()
