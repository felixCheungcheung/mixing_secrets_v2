import os
import sys

root_path = str(sys.argv[1])

for fn in os.listdir(root_path):
    
    if not os.path.isdir(os.path.join(root_path, fn)):
        continue # Not a directory
    if ' ' in fn:
        print(fn)
        r_fn = fn.replace(' ','_')
        print(r_fn)
        os.rename(os.path.join(root_path, fn),os.path.join(root_path, r_fn))
    
