## Getting User Input:
#programName = input("Program name: ")
#BFcode = input("Code: ")

fname = input("File: ")

while(True):
    try:
        with open(fname, 'r') as file:
            BFcode = file.read()
    except FileNotFoundError:
        continue
    else:
        break

## Converting entire string into machine code
conversion = {"+" : "0", "-" : "1", ">" : "2", "<" : "3", "[" : "4", "]" : "5", "." : "6", "," : "7"}
BFcode = [conversion[x] for x in BFcode if x in conversion] 

## Printing machine code
for x in range(len(BFcode)):
    print(BFcode[x], end = "")
print()

fname = fname.replace(".bf", '')
## Saving machine code to specified file 
with open("{}.storm".format(fname), "w+") as file:
    file.write("v2.0 raw")

    for x in range(len(BFcode)):
        if(x % 8 == 0):
            file.write('\n')
        file.write(str(BFcode[x]))
        file.write(" ")
input()

