import argparse
import sys
from connection import Connection
from card import Card

###########################################################
####################### YOUR CODE #########################
###########################################################

def validate_arguments(data) -> bool:
    if "_" in data[1]:   # I assume in saver in getCreators that '_' is the seperator between creator and card name
        print("underscore ('_') is invalid character in creator name")
        return False
    if "_" in data[0]:   
        print("underscore ('_') is invalid character in card name")
        return False   
    return True

def send_data(server_ip, server_port, data: tuple[str]):
    '''
    Send data to server in address (server_ip, server_port).
    '''
    with Connection.connect(server_ip, server_port) as client:
        card = Card.create_from_path(data[0], data[1], data[2], data[3], data[4])
        card.image.encrypt("securepassword")
        card_data = card.serialize()
        client.send_message(card_data)


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('name', type=str,
                        help='card name')
    parser.add_argument('creator', type=str,
                    help='card creator')
    parser.add_argument('riddle', type=str,
                    help='card riddle')
    parser.add_argument('solution', type=str,
                        help='card solution')
    parser.add_argument('path', type=str,
                        help='card image path')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        data = (args.name, args.creator, args.path, args.riddle, args.solution)
        if not validate_arguments(data):            
            exit(1)
        send_data(args.server_ip, args.server_port, data)
        print("Done. Sent all data to server")
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
