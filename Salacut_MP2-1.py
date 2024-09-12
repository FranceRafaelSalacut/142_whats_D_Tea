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
for_loop = []

def assignment(str:str):
    temp = ""
    for char in str:
        if char == "," or char == ";":
            break
        temp = temp + char
    return temp

def var_name(str:str):
    temp = ""
    space = 0
    for char in str:
        if char == "+":
            space+=1
        if char == " ":
            if temp.strip() and not space:
                break
            elif space > 0:
                space-=1
        temp = char + temp
    return temp


def tokenize(str:str) -> list:
    array = statements
    STATE = STATEMENT
    skip = 0

    for line in str:
        # checking for an if statement
        if "if" in line:
            STATE = IF
            array = if_statements
            skip = 2 if "{" in line else 1
            array.append("condition: " + line[line.index("(")+1 : line.index(")")])
            array.append("if statements:")

        elif "else" in line:
            STATE = IF_ELSE
            array = if_statements
            skip = 2 if "{" in line else 1
            array.append("else statements:")
        
        elif "for" in line:
            STATE = FOR
            array = for_loop
            skip = 2 if "{" in line else 1
            content = line[line.index("(")+1 : line.index(")")]
            content = content.split(";")
            equals = content[0].index("=")
            array.append("initializer: " + var_name(reversed(content[0][:equals])) + assignment(content[0][equals:]))
            array.append("condition: " + content[1]) 
            array.append("update:" +  content[2])
            array.append("for statements:")

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
            
    if for_loop:
        print("for:")
        for line in for_loop:
            print(line)

def main():
    num = int(input())

    lines = []
    for x in range(0, num):
        lines.append(input())

    result = tokenize(lines)
    output(result)

main()
