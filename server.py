import socket
import time
import pickle


HEADERSIZE_ONE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1243))
s.listen(5)

def send_dict(dict_to_send, client):
    msg = pickle.dumps(dict_to_send)
    msg = bytes(f"{len(msg):<{HEADERSIZE_ONE}}", 'utf-8') + msg
    print("itt")
    client.send(msg)
bikazo = True
ez = "a"
while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    if bikazo:
        d = {1:"hi", 2: "there"}
        send_dict(d, clientsocket)

    full_msg = b''
    new_msg = True
    while True:
        msg = clientsocket.recv(16)
        if new_msg:
            msglen = int(msg[:HEADERSIZE_ONE])
            new_msg = False

        full_msg += msg

        if len(full_msg) - HEADERSIZE_ONE == msglen:
            result = pickle.loads(full_msg[HEADERSIZE_ONE:])
            print(result)
            new_msg = True
            full_msg = b""


            result[ez] = "fa"

            send_dict(result,clientsocket)
            ez += "a"
            continue
