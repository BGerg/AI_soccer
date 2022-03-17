import socket
import pickle

HEADERSIZE_ONE = 10

my_username = "blue_team"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1243))

def send_dict(dict_to_send, client):
    msg = pickle.dumps(dict_to_send)
    msg = bytes(f"{len(msg):<{HEADERSIZE_ONE}}", 'utf-8') + msg
    print("itt")
    client.send(msg)
ez = "a"

while True:
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            msglen = int(msg[:HEADERSIZE_ONE])
            new_msg = False
        full_msg += msg

        if len(full_msg)-HEADERSIZE_ONE == msglen:
            result = pickle.loads(full_msg[HEADERSIZE_ONE:])
            print(result)
            new_msg = True
            full_msg = b""

            result[ez] = "fa"

            send_dict(result,s)
            ez += "a"













