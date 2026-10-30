# print([n for n in dir("abc") if n.startswith("st")])

# import numpy as np
# print([n for n in dir(np) if n.startswith("lin")])

# print( [n for n in dir(np) if "su" in n] )

# print([n for n in dir(np) if not n.startswith("_")])

# import numpy as np
# #help(np.linspace)
# import inspect
# print(inspect.signature(np.linspace))

# name= dir("abc")
# for n in name:
#     print (n)

import cv2
import pandas as pd
#print([ n for n in dir(cv2.VideoCapture) if not n.startswith  ("_")])

dir_result = ([ n for n in dir(cv2) if "prop" in n.lower()])
print ("\n".join (dir_result))
#class_list = ([n for n in dir(pd) if not n.startswith  ("_")] )
#print("\n".join(class_list))
