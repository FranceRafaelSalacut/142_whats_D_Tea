'''
ONLINE RESOURCES

https://builtin.com/software-engineering-perspectives/python-substring-indexof


'''
# doin states here
STATEMENT = 1
IF = 2
IF_ELSE = 3
FOR = 4
memory = []
statements = []
if_statements = []

def assignment(str:str):
    temp = ""
    for char in str:
        if char == "," or char == ";":
            break
        temp = temp + char
    return temp

def var_name(str:str):
    temp = ""
    space = 1
    for char in str:
        if char == " ":
            if space:
                space = 0
            else:
                break
        temp = char + temp
    return temp


def tokenize(str:str) -> list:
    array = statements
    STATE = STATEMENT
    skip = 0
    count = 0

    for line in str:
        # checking for an if statement
        if "if" in line:
            STATE = IF
            array = if_statements
            skip = 2 if "{" in line else 1
            array.append("condition: " + line[line.index("(")+1 : line.index(")")])
            array.append("if satements:")

        elif "else" in line:
            STATE = IF_ELSE
            array = if_statements
            skip = 2 if "{" in line else 1
            array.append("else statements:")
            

        # checking if there is a print statement
        elif "cin" in line:
            array.append(line.replace(";",""))

        # checking if there is a varibale assignment
        elif "=" in line:
            for index,token in enumerate(line):
                if token == "=":
                    temp = var_name(reversed(line[:index])) + assignment(line[index:])
                    array.append(''.join(temp))

        # checking for an end of conditional statement
        elif skip == 1: 
            skip = 0
            STATE = STATEMENT
            array = statements

         # checking for an end of conditional statement
        elif "}" in line: 
            skip = 0
            STATE = STATEMENT
            array = statements


    return(array)



def output(str:str) -> None:
    if statements:
        print("statements:")
        for line in statements:
            print(line)

    if if_statements:
        print("if:")
        for line in if_statements:
            print(line)

def main():
    num = int(input())

    lines = []
    for x in range(0, num):
        lines.append(input())

    result = tokenize(lines)
    output(result)

main()
