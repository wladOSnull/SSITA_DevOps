import os, sys

def create_directories():
    
    path_name = os.path.join(sys.argv[1], sys.argv[2])
    
    for iter in range(int(sys.argv[3])):
        os.mkdir(path_name+str(iter+1), int('0o'+sys.argv[4], base=8))
        
print("mod is: ", int(sys.argv[4]))

try:
    create_directories()
except OSError:
    print("Error: the folder(s) already exist")
else:
    print("Folder(s) is(are) created")

### usage
##################################################
'''
Executing script / creating folders:
~ python3 hw1.py ./ usr 5 551

Deleting created folders:
~ rm -drf usr*
'''