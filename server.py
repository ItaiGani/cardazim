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
            data = conn.recv(4096)
            if not data:
                 break
            from_client += data.decode()
        print (f'From client: {from_client}')
        conn.close()
        print('client disconnected and shutdown')
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
        set_server(args.server_ip, args.server_port)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())