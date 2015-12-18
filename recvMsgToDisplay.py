#!/usr/bin/python3

import socket
import select
import os
import stat
from displayPacket import DisplayPacket


class RecvMsg:
    server_address = '/run/lcd/socket'
    max_connection = 2

    def __init__(self, sock_path):
        self.server_address = sock_path
        # Make sure the socket does not already exist
        try:
            os.unlink(self.server_address)
        except OSError:
            if os.path.exists(self.server_address):
                raise
        
        # Create a UDS socket
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
   
        # Bind the socket to the port
        print('starting up on', self.server_address)#, file=sys.stderr)
        self.sock.bind(self.server_address)

        os.chmod(self.server_address,stat.S_IRWXO)

        self.sock.listen(self.max_connection)

    def __del__(self):
        self.sock.close()

    def recvMsg(self, timeout=1):
        dp = DisplayPacket()
        client = None
        try:
            rlist, wlist, elist = [self.sock], [], [self.sock]
            rlist, wlist, elist = select.select(rlist, wlist, elist, timeout)

            if self.sock in rlist:
                print('fd is selected')#, file=sys.stderr)
                client, addr = self.sock.accept() 
                data = client.recvfrom(200)
                dp.unpack(data[0])
                print('received user :"{}" message :"{}"'.format(dp.user,dp.message))#, file=sys.stderr)
                if len(data)>1:
                    print('sending data back to the client')#, file=sys.stderr)
                    client.sendall(b"OK")
                    dp.message = dp.message.replace('\r', '')# remove \r, because it is not well displayed on the display
                else:
                    print('no more data from', addr)#, file=sys.stderr)
            if self.sock in elist:
                print('Seems to have a problem with the socket')#, file=sys.stderr)
        finally:
            # Clean up the connection
            if client is not None:
                client.close()
        return dp.user, dp.message


if __name__ == '__main__':
    rm = RecvMsg()
    while rm.recvMsg() == (None, None):
        print("No message")
