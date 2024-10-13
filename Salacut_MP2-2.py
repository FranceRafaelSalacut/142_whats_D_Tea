'''
ONLINE RESOURCES

https://builtin.com/software-engineering-perspectives/python-substring-indexof
https://www.w3resource.com/python-exercises/string/python-data-type-string-exercise-27.php
https://www.mygreatlearning.com/blog/python-string-split-method/#:~:text=By%20using%20the%20newline%20character,the%20string%20into%20separate%20lines.&text=In%20this%20example%2C%20the%20string%20text%20contains%20three%20lines%20separated,creates%20a%20list%20of%20lines.


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
        if char == " " or char == ";":
            if temp.strip() and not space:
                break
            elif space > 0:
                space-=1
        temp = char + temp
    return temp

def test(x,y):
    #print(f"{x} on {y}")
    pass

def output(str:str):
    print(tw.dedent(str.replace(";","")))


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
            content = content.split(":")
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
            if skip == 1: 
                skip = 0
                if STATE == IF_IN_FOR:
                    STATE = FOR
                    print("for statements continued:")
                else:
                    STATE = STATEMENT
            print(tw.dedent(line).replace(";", ""))
        
        # checking if there is a varibale assignment
        elif "=" in line:
            if STATE == STATEMENT:
                STATE = STATEMENT_PRINT
                print("statements:")
            if skip == 1: 
                skip = 0
                if STATE == IF_IN_FOR:
                    STATE = FOR
                    print("for statements continued:")
                else:
                    STATE = STATEMENT
            for index,token in enumerate(line):
                if token == "=":
                    temp = var_name(reversed(line[:index])) + assignment(line[index:])
                    print(''.join(temp))

         # checking for an end of conditional statement
        elif "}" in line: 
            skip = 0
            if STATE == IF_IN_FOR:
                STATE = FOR
                print("for statements continued:")
            else:
                STATE = STATEMENT
        else:
            if "int" in line or "float" in line or "double" in line or "bool" in line:
                continue
            if STATE == STATEMENT:
                STATE = STATEMENT_PRINT
                print("statements:")
            print(tw.dedent(line).replace(";",""))
            test("none", line)



def main():
    num = int(input())

    lines = []
    for _ in range(0, num):
        line = input()
        #formatting the code correctly for the one liners. 
        if "for" in line:
            temp = line[line.index("(")+1 : line.index(")")]
            temp2 = temp.replace(";", ":")
            line = line.replace(temp, temp2)

        if ";" in line:
            line = line.replace(";", ";\n")

        if "){" in line:
            line = line.replace("){", "){\n")
        elif ")" in line:
            line = line.replace(")", ")\n")

        if "}" in line:
            line = line.replace("}", "\n}")

        
        #removing whitelines and empty strings
        line = line.split("\n")
        for text in line:
            if text and text.strip():
                lines.append(text)
                
    tokenize(lines)
main()
