import math, re, sys
step_by_step = False # Prints steps to assure correct control flow.
debug = False # Verbose output for testing stages. 
tasks_T = []
processors_P = []
timeLimit_D = 0
target_S = -math.inf
def parseInput(input):
    global tasks_T
    global processors_P
    global timeLimit_D
    global target_S
    fileOK = False
    try: 
        file = open(input, "r") # Read file.
        fileOK = True
    except:
        print("Fix: File does not exist, or access to file is denied. Check name and path of file.") # It's a valid path, but who knows if it exists!
    if fileOK == True:
        i = 0
        j = 0
        for line in file: # Separate via lines
            separatedValues = line.split(' ') # Separate via spaces.
            for value in separatedValues: # Iterate over values.
                valid = re.search(r'^[0-9]+(\.[0-9]+)?$', value) # Return if value in format dn(.dn) (can be int or float)
                value = value.split('\n')[0] # Remove any pesky trailing newlines.
                if valid != None: # If it is a valid value...
                    if i is 0:
                        tasks_T.append(float(value)) # Populate tasks.
                    elif i is 1:
                        processors_P.append(float(value)) # Populate processors.
                    elif i is 2:
                        if j is 0:
                            timeLimit_D = float(value) # Set time limit.
                            j = 1
                        else:
                            target_S = float(value) # Set target.
            hasContent = re.search(r'[0-9]+', line) 
            if hasContent != None: # If the line had any numbers...
                i+=1 # Increment per new line to populate correctly.
    if step_by_step: print("Step #1 Input ingested.")
def please():
        print("Please supply a valid path to the input file. Check name and path of file.")
def ingest_input(argv):
    global step_by_step
    global debug
    if len(argv) > 1:
        path = argv[1] # The 1st option (after this containing file) in cmd should be path to plaintext input.
        valid = re.search(r"^(\/?[&\+\"\'\.a-zA-Z0-9_-]+\/?)+$", path) # Make sure it is a valid path string.
        if valid != None:
            if len(argv)>2:
                if argv[2] == '--sbs':
                    step_by_step = True
                if len(argv)>3:
                    if argv[3] == '--verbose':
                        debug = True
            parseInput(path)
        else:
            please() 
    else:
        please()