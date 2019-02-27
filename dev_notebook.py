#%%
import re

correct_instructions = []
with open("input_files/correct_instructions.txt") as file:
    for line in file.readlines():
        #print(line)
        if line.startswith('#'):
            continue
        rule = line.split('#')[0]
        if rule.isspace():
            continue
        correct_instructions.append(re.sub('[\s]+', '', rule))


print(correct_instructions)

incorrect_instructions = []
with open("input_files/incorrect_instructions.txt") as file:
    for line in file.readlines():
        #print(line)
        if line.startswith('#'):
            continue
        rule = line.split('#')[0]
        if rule.isspace():
            continue
        incorrect_instructions.append(re.sub('[\s]+', '', rule))

print(incorrect_instructions)
#%%

def check_instruction(instruction):
    inst_split = instruction.split("=")
    #print(len(inst_split))
    if len(inst_split) != 2:
        return (False)
    inst_split[0] = inst_split[0][:-1] if inst_split[0][-1] == "<" else inst_split[0]
    if inst_split[1][0] != ">":
        return (False)
    
    #alphabet = "ABCDEFGHIJKLMNOP"
    #operators = "+!|^()<=>"
    #if instruction[0] != "!":
    #    return (False)
    return(True)



for elem in incorrect_instructions:
    print(elem, check_instruction(elem))
    

#%%
