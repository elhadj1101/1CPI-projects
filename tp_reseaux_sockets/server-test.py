import socket
from operator import add, sub, mul, truediv, pow
import time


def calculate(operand1, operand2, op):
    operations = {"+": add, "-": sub, "*": mul, "/": truediv, "^": pow}
    if op not in operations:
        raise ValueError("Invalid operator. Valid operators are: +, -, *, /")
    return operations[op](operand1, operand2)


def get_operation_elements(operation):
    for i in operation:
        if i not in "1234567890":
            operand1 = operation[: operation.index(i)]

            operand2 = operation[operation.index(i) + 1 :]

            op = i

    return [operand1, op, operand2]


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

myadd = "localhost"
myport = 10000

s.bind((myadd, myport))
s.listen(3)

sData, sendAdd = s.accept()


resp = "y"
while resp != "n":
    operation = sData.recv(1024).decode()
    operand1, op, operand2 = get_operation_elements(operation)
    if not operand1.isdigit() or not operand2.isdigit():
        sData.send("operation in wrong format  , try again".encode())
    else:
        result = calculate(int(operand1), int(operand2), op)

        print(f"the result that will be sent to the client : {result}")

        time.sleep(2)
        sData.send(str(result).encode())
    print("waiting for continuity response ... ")
    resp = sData.recv(1024).decode()


s.close()
