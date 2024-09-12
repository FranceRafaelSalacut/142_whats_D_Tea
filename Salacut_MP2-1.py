'''
ONLINE RESOURCES

https://stackoverflow.com/questions/6531482/how-to-check-if-a-string-contains-an-element-from-a-list-in-python


'''



datatype = ["int", "char", "float", "double"]
memory = []

def tokenize(str:str) :
    for x in str:
        line = x.split()
        print(line)

def output(str:str) -> None:
    for x in str:
        print(x)

def main():
    num = int(input())

    for x in range(0, num):
        memory.append(input())

    tokenize(memory)

main()
