'''
ONLINE RESOURCES

https://builtin.com/software-engineering-perspectives/python-substring-indexof
https://www.w3resource.com/python-exercises/string/python-data-type-string-exercise-27.php
https://www.mygreatlearning.com/blog/python-string-split-method/#:~:text=By%20using%20the%20newline%20character,the%20string%20into%20separate%20lines.&text=In%20this%20example%2C%20the%20string%20text%20contains%20three%20lines%20separated,creates%20a%20list%20of%20lines.


'''
import textwrap as tw
import re
import sympy as sp

# doin states here
STATEMENT = 1
STATEMENT_PRINT = 2
IF = 3
IF_ELSE = 4
FOR = 5
IF_IN_FOR = 6
CONDITION_COUNT = 0
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

def print_statements(STATE, tokenized, line, inner_for_loop=False):
    if "++" in line or "--" in line:
        if inner_for_loop:
            tokenized.append(''.join(line).replace(";","").replace(" ",""))
        tokenized[STATE].append(''.join(line).replace(";","").replace(" ",""))
        return
    for index,token in enumerate(line):
        if token == "=":
            if line.count("=") > 1:
                if inner_for_loop:
                    tokenized.append(''.join(line))
                tokenized[STATE].append(''.join(line))
                return
            temp = var_name(reversed(line[:index])) + assignment(line[index:])
            #print(f"ff{STATE}")
            #print(''.join(temp))
            if inner_for_loop: 
                tokenized.append(''.join(temp))
            else:
                tokenized[STATE].append(''.join(temp))

    if inner_for_loop:
        return tokenized

def get_assignment(line):
    #print(line)
    if ">=" in line:
        line = line.replace(">","")
    if "<=" in line:
        line = line.replace("<","")
    for index,token in enumerate(line):
        if token == "=" or token == ">" or token == "<":
            try:
                return int(assignment(line[index:]).replace(token,""))
            except:
                return assignment(line[index:]).replace(token,"")
        
def tokenize(str:str) -> dict:
    global CONDITION_COUNT
    #array = statements
    STATE = STATEMENT
    skip = 0
    inner_loop_flag = False
    inner_skip = 0
    inner_for = []
    tokenized = {STATEMENT:[], 
                 IF: [],
                 IF_ELSE: [],
                 FOR: [],
                 IF_IN_FOR: []}

    for line in str:
        # checking for an if statement
        if "if" in line:
            if STATE == FOR:
                STATE = IF_IN_FOR
            else:
                STATE = IF
            skip = 2 if "{" in line else 1
            #print("if:")
            tokenized[STATE].append("condition: " + line[line.index("(")+1 : line.index(")")])
            #print("if statements:")
            #tokenized[STATE].append(line[line.index("(")+1 : line.index(")")])
            CONDITION_COUNT+=1

        elif "else" in line:
            STATE = IF_ELSE
            skip = 2 if "{" in line else 1
            #print("else statements:")
        
        elif "for" in line:
            STATE = FOR
            content = line[line.index("(")+1 : line.index(")")]
            content = content.split(":")
            equals = content[0].index("=")

            if inner_loop_flag:
                inner_skip = 2 if "{" in line else 1
                inner_loop_flag = False
                inner_for.append("initializer: " + var_name(reversed(content[0][:equals])) + assignment(content[0][equals:]))
                inner_for.append("condition:" + content[1]) 
                inner_for.append("update:" +  content[2])
            else:
                skip = 2 if "{" in line else 1
                tokenized[STATE].append("initializer: " + var_name(reversed(content[0][:equals])) + assignment(content[0][equals:]))
                tokenized[STATE].append("condition:" + content[1]) 
                tokenized[STATE].append("update:" +  content[2])
                inner_loop_flag = True
            
            
            #print("for:")
            
            #print("for statements:")

        # checking if there is a print statement or input statement
        elif "cin" in line or "cout" in line:
            if STATE == STATEMENT:
                #STATE = STATEMENT_PRINT
                #print("statements:")
                print_statements(STATE, tokenized, line)
            if skip == 1 and inner_skip == 0: 
                skip = 0
                inner_loop_flag = False
                if STATE == IF_IN_FOR:
                    STATE = FOR
                    print("for statements continued:")
                else:
                    STATE = STATEMENT

            if inner_skip:
                if inner_skip == 1:
                    inner_skip = 0
                    inner_for.append(tw.dedent(line).replace(";", ""))
                    tokenized[STATE].append(inner_for)
                    inner_for = []

                    if skip == 1:
                        skip = 0
                        inner_loop_flag = False
                        STATE = STATEMENT
                else:
                    inner_for.append(tw.dedent(line).replace(";", ""))

            else:
                #print(tw.dedent(line).replace(";", ""))
                tokenized[STATE].append(tw.dedent(line).replace(";", ""))
        
        # checking if there is a variable assignment
        elif "=" in line or "--" in line or "++" in line:
            #print(f" this here {line} - {STATE}")
            if STATE == STATEMENT:
                #STATE = STATEMENT_PRINT
                print_statements(STATE, tokenized, line)
                #print("statements:")
            if skip == 1 and inner_skip == 0: 
                print_statements(STATE, tokenized, line)
                skip = 0
                inner_loop_flag = False
                if STATE == IF_IN_FOR:
                    STATE = FOR
                    print("for statements continued:")
                else:
                    STATE = STATEMENT
            if STATE == IF:
                print_statements(STATE, tokenized, line)

            if STATE == IF_ELSE:
                print_statements(STATE, tokenized, line)

            if STATE == FOR:
                if inner_skip:
                    if inner_skip == 1:
                        inner_skip = 0
                        inner_for = print_statements(STATE, inner_for, line, True)
                        tokenized[STATE].append(inner_for)
                        inner_for = []

                        if skip == 1:
                            skip = 0
                            inner_loop_flag = False
                            STATE = STATEMENT
                    else:
                        inner_for = print_statements(STATE, inner_for, line, True)

                else:
                    print_statements(STATE, tokenized, line, False)

         # checking for an end of conditional statement
        elif "}" in line: 
            if skip == 2 and inner_skip == 0:
                inner_loop_flag = False
                skip = 0

            if inner_skip == 2:
                inner_skip = 0
                tokenized[STATE].append(inner_for)
                inner_for = []

                if skip == 1:
                    skip = 0
                    STATE = STATEMENT

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
                #print("statements:")
            #print(tw.dedent(line).replace(";",""))
            


    return tokenized

def operator_count(string, count):
    ops = ["+", "-", "*", "/", "=", ">", "<"]
    itertr = ["+=","-=", "*=", "/=", "++", "--"]
    for itr in itertr:
        if itr in string:
            string = string.replace(itr,"")
    for op in ops:
        if string.count(op):
            count+=string.count(op)

    return count

def check_for(For):
    count = 0
    for x in For:
        if "initializer" in x:
            count+=1
    if count == 1:
        return False
    
    return True

def find_loops(For):
    For_loops = []
    temp = []
    for x in For:
        if "initializer" in x:
            if temp:
                For_loops.append(temp)
            temp = []
            temp.append(x)
        else:
            temp.append(x)
    For_loops.append(temp)
    return For_loops

def count_T_Fors(For, count):
    For_loops = find_loops(For)
    #print(For_loops)

    counted = sp.simplify(0)

    for x in For_loops:
        T_n = count_T_For(x, 0)
        counted+=sp.simplify(T_n)

    counted+=sp.simplify(count)

    counted = str(counted)
    counted = counted.replace("**","^")
    counted = counted.replace("*","")
    return f"T(n) = {counted}"

def count_T_For(For, count):
    inner_loop_count = sp.simplify(0)
    outer_loop_count = 0
    n_value = True
    i = 0
    n = 0
    log = 0
    n_dom = 0
    num_i = 0
    temp = None
    for x in For:
        if "initializer" in x:
            outer_loop_count+=1
            i = get_assignment(x)
        elif "condition" in x:
            x = x.replace("condition","")
            outer_loop_count+=1
            inner_loop_count+=1
            if ">=" in x or "<=" in x:
                if "n" not in x:
                    n_value = False
                    n = get_assignment(x)
                else:
                    temp = x
            else:
                if "n" in x:
                    n = -1
                    temp = "= n-1"
                else:
                    n_value = False
                    n = get_assignment(x) - 1

            if n <= 1 and i == " n":
                #print(f"{outer_loop_count} + {count}")
                return f"{outer_loop_count + count}"
            
            if x.count("i") > 1:
                num_i = x.count("i")
                
        elif "update" in x:
            inner_loop_count+=1
            if "*=" in x or "/=" in x:
                log = get_assignment(x)
                i = 0 
            elif "+=" in x or "-=" in x:
                n_dom = get_assignment(x)
                i = 1
            elif "--" in x:
                return "infinite"
        elif type(x) == list:
            inner_loop_count+=(sp.simplify(count_T_For(x,0)))
        else:
            #print(x)
            if "+=" in x or "-=" in x or "--" in x or "++" in x or "*=" in x or "/=" in x:
                inner_loop_count+=1
                inner_loop_count = operator_count(x, inner_loop_count)
            elif "=" in x:
                #inner_loop_count+=1
                if re.findall(r'-\s*-\d+|-\d+', x):
                    inner_loop_count-=1
                inner_loop_count = operator_count(x, inner_loop_count)
            elif "cin" in x or "cout" in x:
                inner_loop_count+=1
            #print(f"count = {count}")

    #print(f"{inner_loop_count} -- {outer_loop_count} -- {i} -- {n} -- {count} -- {log}")

    if num_i:
        if num_i == 2:
            return f"{inner_loop_count+1} sqrt(n) + {outer_loop_count+1+count}"
        elif num_i == 3:
            return f"{inner_loop_count+2} cubert(n) + {outer_loop_count+2+count}"

    if not str(i).isnumeric():
        n = get_assignment(temp)
        if n != " n-1":
            #print(f"here {n}")
            inner_loop_count = operator_count(n, inner_loop_count)
            outer_loop_count = operator_count(n, outer_loop_count)
        outer_loop_count = operator_count(i, outer_loop_count)
        n = sp.simplify(n)
        i = sp.simplify(i)
        #print(i)
        #print(f"{inner_loop_count} -- {outer_loop_count} -- {i} -- {n} -- {count} -- {log}")
        return f"{sp.simplify(inner_loop_count*(n-i+1) + outer_loop_count + count)}".replace("*","")
    
    if n_value:
        if not log:
            if not n_dom:
                formula1 = (n-i)+1
                if not formula1:
                    en = sp.symbols('n')
                    #return f"{inner_loop_count}n + {outer_loop_count + count}"
                    return sp.expand((inner_loop_count*en) + outer_loop_count + count)
                else:
                    formula2 = inner_loop_count * formula1
                    formula2 = formula2 + outer_loop_count + count

                    sign = "+"
                    if formula2 < 0:
                        sign = "-"
                        formula2 = formula2 * -1

                    return f"{inner_loop_count}n {sign} {formula2}"
            else:
                formula1 = (n-i+1)
                if not formula1:
                    return f"{inner_loop_count}n/{n_dom} + {outer_loop_count + count}"
                else:
                    formula2 = inner_loop_count * formula1
                    formula2 = formula2 + outer_loop_count + count

                    sign = "+"
                    if formula2 < 0:
                        sign = "-"
                        formula2 = formula2 * -1

                    return f"{inner_loop_count}n/{n_dom} {sign} {formula2}"
        else:
            formula1 = (n-i+1)
            formula2 = (inner_loop_count*formula1) + outer_loop_count + count
            return f"{inner_loop_count} log({log}) n + {formula2}"
    else:
        formula1 = (inner_loop_count * ((n-i)+1)) + outer_loop_count + count
        return f"{formula1}"

def count_T(token):
    count = 0
    
    statements = token[STATEMENT]
    If = token[IF]
    If_else = token[IF_ELSE]
    For = token[FOR]
    If_in_for = token[IF_IN_FOR]

    print(f"{statements}\n{If}\n{If_else}\n{For}\n{If_in_for}\n")

    for x in statements:
        #print(x)
        if "+=" in x or "-=" in x or "--" in x or "++" in x:
            count+=1
        elif "=" in x:
            #count+=1
            if re.findall(r'-\s*-\d+|-\d+', x):
                count-=1
            count = operator_count(x, count)
        elif "cin" in x or "cout" in x:
            count+=1
        #print(f"count = {count}")

    if_len = len(If) - CONDITION_COUNT
    else_len = len(If_else)

    if if_len > else_len:
        for x in If:
            #print(x)
            if "condition" in x:
                count+=1
            else:
                if "+=" in x or "-=" in x or "--" in x or "++" in x:
                    count+=1
                elif ">" in x or "<" in x or ">=" in x or "<=" in x:
                    count+=1
                elif "=" in x:
                    #count+=1
                    if re.findall(r'-\s*-\d+|-\d+', x):
                        count-=1
                    count = operator_count(x, count)
                elif "cin" in x or "cout" in x:
                    count+=1
                #print(f"count = {count}")
    else:
        count+=CONDITION_COUNT
        for x in If_else:
            #print(x)
            if "+=" in x or "-=" in x or "--" in x or "++" in x:
                ount+=1
            elif "=" in x:
                #count+=1
                if re.findall(r'-\s*-\d+|-\d+', x):
                    count-=1
                count = operator_count(x, count)
            elif "cin" in x or "cout" in x:
                count+=1
            #print(f"count = {count}")

    if not len(For):
        return f"T(n) = {count}"
    
    if check_for(For):
        return count_T_Fors(For, count)
    
    tempo = count_T_For(For, count)
    tempo = str(tempo)
    tempo = tempo.replace("**","^")
    tempo = tempo.replace("*","")
    return f"T(n) = {tempo}"
    
    return 0

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

        if "){" in line or ") {" in line:
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
    tokens = tokenize(lines)
    print(count_T(tokens))

main()
