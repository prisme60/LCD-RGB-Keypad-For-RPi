#!/usr/bin/python3

import socket
import sys
from displayPacket import DisplayPacket

def sendMsg(message, user="unknown"):
    sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)

    server_address = "/run/lcd/socket"
    try:
        sock.connect(server_address)
    except socket.error as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    try:
        # Send data
        dp = DisplayPacket(user, message)
        print('sending user={} message={}'.format(dp.user, dp.message), file=sys.stderr)
        data = dp.pack()
        print(repr(data))
        sock.sendall(data)
    
        data = sock.recv(200)
        print('received "{!r}"'.format(data), file=sys.stderr)
        return len(data) > 1 and data == b'OK'

    finally:
        print('closing socket', file=sys.stderr)
        sock.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        sendMsg(" ".join(sys.argv[1:]), 'CF')
    else:
        sendMsg('Message par défaut', 'CF')
