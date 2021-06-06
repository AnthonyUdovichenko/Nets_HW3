import socket
from sys import argv
import struct

_, host, port = argv

print('Server started')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, int(port)))

max_number = -1
received = dict()

while True:
    data, addr = sock.recvfrom(1024)
    text, number = struct.unpack('<480si', data)
    if number in received:
        continue
    received[number] = text.decode('ascii')
    if number == max_number + 1:
        if number > 0:
            print(received[number], end='')
        else:
            print('Client is connected')
            print('All incoming messages from client will be printed in the right order')
        max_number = number
        while max_number + 1 in received:
            print(received[max_number + 1], end='')
            max_number += 1
    elif number == -1:
        sock.sendto(struct.pack('<i', -1), addr)
        break
    sock.sendto(struct.pack('<i', max_number + 1), addr)

print('Client closed connection')

sock.close()

print('Server is stopped')
