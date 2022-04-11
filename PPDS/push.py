#!/usr/bin/env python 
import os
import sys

if len(sys.argv) != 2:
    print("usage: push.py \"<commit msg>\"")

err = os.system(f'git add . && git commit -m \"{sys.argv[1]}\" && git push')
if err:
    print("NONZERO EXIT CODE: ", err)
else:
    print("PUSH SUCCEEDED")

os.system("git status")

    


