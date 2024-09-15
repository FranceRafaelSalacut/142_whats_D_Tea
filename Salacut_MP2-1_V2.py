'''
ONLINE RESOURCES

https://builtin.com/software-engineering-perspectives/python-substring-indexof


'''
import textwrap as tw

# doin states here
STATEMENT = 1
STATEMENT_PRINT = 2
IF = 3
IF_ELSE = 4
FOR = 5
IF_IN_FOR = 6
memory = []

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

def test(x,y):
    #print(f"{x} on {y}")
    pass



def tokenize(str:str) -> list:
    #array = statements
    STATE = STATEMENT
    skip = 0

    for line in str:
        # checking for an if statement
        if "if" in line:
            if STATE == FOR:
                STATE = IF_IN_FOR
            else:
                STATE = IF
            skip = 2 if "{" in line else 1
            print("if:")
            print("condition: " + line[line.index("(")+1 : line.index(")")])
            print("if statements:")

        elif "else" in line:
            STATE = IF_ELSE
            skip = 2 if "{" in line else 1
            print("else statements:")
        
        elif "for" in line:
            STATE = FOR
            skip = 2 if "{" in line else 1
            content = line[line.index("(")+1 : line.index(")")]
            content = content.split(";")
            equals = content[0].index("=")
            print("for:")
            print("initializer: " + var_name(reversed(content[0][:equals])) + assignment(content[0][equals:]))
            print("condition:" + content[1]) 
            print("update:" +  content[2])
            print("for statements:")

        # checking if there is a print statement or input statement
        elif "cin" in line or "cout" in line:
            if STATE == STATEMENT:
                STATE = STATEMENT_PRINT
                print("statements:")
            print(tw.dedent(line.replace(";","")))
        
        # checking if there is a varibale assignment
        elif "=" in line:
            if STATE == STATEMENT:
                STATE = STATEMENT_PRINT
                print("statements:")
            for index,token in enumerate(line):
                if token == "=":
                    temp = var_name(reversed(line[:index])) + assignment(line[index:])
                    print(''.join(temp))

        # checking for an end of conditional statement
        elif skip == 1: 
            skip = 0
            if STATE == IF_IN_FOR:
                STATE = FOR
                print("for statements continued:")
            else:
                STATE = STATEMENT

         # checking for an end of conditional statement
        elif "}" in line: 
            skip = 0
            if STATE == IF_IN_FOR:
                STATE = FOR
                print("for statements continued:")
            else:
                STATE = STATEMENT
        else:
            print(line)
            test("none", line)

        



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

    #result = tokenize(lines)
    #output(result)

    tokenize(lines)

main()
