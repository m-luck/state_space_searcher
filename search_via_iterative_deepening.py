import anytree as at, sys
path = sys.argv[1] # The 1st option (after this containing file) in cmd should be path to plaintext input
file = open(path, "r") # Open this path as a file, read-only
for line in file:
    line = 