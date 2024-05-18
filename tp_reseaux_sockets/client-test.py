import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

dest_ip = "localhost"
dest_port = 10000

s.connect((dest_ip, dest_port))


resp = ""
while resp != "n":
    first = input("enter first operand : ")
    op = input("enter the operation : ")
    second = input("enter the second operand : ")
    operation = first + op + second

    s.sendto(operation.encode(), (dest_ip, dest_port))
    result = s.recv(1024)
    if result.decode().isdigit():
        print(f"the result of :  {first} {op} {second}  = {result.decode()}")
    else:
        print(result.decode())
    resp = input("do you want to continue ? y/n : ")
    s.sendto(resp.encode(), (dest_ip, dest_port))


s.close()
