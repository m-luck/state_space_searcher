import anytree as at, re, sys
tasks = []
processors = []
def parseInput(input):
    global tasks
    global processors
    file = open(input, "r")
    i = 0
    for line in file:
        separatedValues = line.split(' ') 
        for value in separatedValues:
            valid = re.search(r'^[0-9]+(\.[0-9]+)?$', value)
            if valid != None:
                switch = {
                    0: 
                    1:
                    2:
                }
        i+=1
            # assert(float(value)>0)
def checkInput(): 
    if len(sys.argv) > 1:
        path = sys.argv[1] # The 1st option (after this containing file) in cmd should be path to plaintext input
        valid = re.search(r"^(\/?[&\+\"\'\.a-zA-Z0-9_-]+\/?)+$", path)
        if valid != None:
            parseInput(path)
    else:
        print("Please supply a path to the input file.")
checkInput()
