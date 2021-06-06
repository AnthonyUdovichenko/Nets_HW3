import socket
from sys import argv
import struct
import textwrap

_, host, port = argv

print('Client started')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((host, int(port)))
sock.setblocking(False)

print('Connection is not established yet. Any input data will be lost')
print('If this takes too long, check if server is working')

sent = dict()

while True:
    pck = struct.pack('<480si', b'Incoming connection', 0)
    sock.send(pck)
    sent[0] = pck
    try:
        data = sock.recv(1024)
        break
    except BlockingIOError:
        pass

print('Connection established')

number = 0

print('Now you can type messages to server')
print('Type \'exit\' to close connection')

while True:
    try:
        text = input()
    except EOFError:
        text = 'exit'
    if text == 'exit':
        print('Do you want to close connection? (Y/anything else)')
        try:
            answer = input()
        except EOFError:
            answer = 'Y'
        if answer != 'Y':
            continue
        pck = struct.pack('<480si', b'Exit', -1)
        while True:
            sock.send(pck)
            try:
                data = sock.recv(1024)
                req_number = struct.unpack('<i', data)[0]
                if req_number == -1:
                    exit(0)
                if req_number >= number + 1:
                    continue
                sock.send(sent[req_number])
            except BlockingIOError:
                pass
    split_text = textwrap.fill(text, width=450).split('\n')
    split_text.append('\n')
    for part in split_text:
        number += 1
        pck = struct.pack('<480si', part.encode('ascii'), number)
        sock.send(pck)
        sent[number] = pck
        while True:
            try:
                data = sock.recv(1024)
                req_number = struct.unpack('<i', data)[0]
                if req_number >= number + 1:
                    break
                sock.send(sent[req_number])
            except BlockingIOError:
                break
