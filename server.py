import argparse
import sys
import socket
import threading
from connection import Connection


def handle_client(conn: Connection):
    message = conn.receive_message()
    print(f"current thread id = {threading.get_native_id()}")
    print (f'Recieved data: {message}')
    conn.close()

def run_server(server_ip, server_port):
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((server_ip, server_port))
    serv.listen(5)
    while True:
        conn, addr = serv.accept()
        conn = Connection(conn)
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.start()

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