import argparse
import sys
import socket
import struct
import os

def run_server(server_ip, server_port):
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((server_ip, server_port))
    serv.listen(5)
    while True:
        conn, addr = serv.accept()
        from_client = ''
        msg_len = conn.recv(4)
        tup = struct.unpack("<I", msg_len)[0]
        while True:
            data = conn.recv(4096)          # dont want to recv len of full msg, cause it can be really long
                                            # No need to allocate so much memory, maybe define it as a function of length instead of fixed size
            if not data:
                 break
            from_client += data.decode()
        print (f'Recieved data: {from_client}')
        conn.close()
        if from_client == "close":      # was not mentioned in instruction, but pretty nnoying to use ctr + c t close every time
            serv.close()
            print("Server has been closed")
            return

def get_args():
    parser = argparse.ArgumentParser(description='setup server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())