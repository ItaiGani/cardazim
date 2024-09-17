import socket
import struct


HEADER_LEN = 4


class Connection():

# ----------------------------------------------------------------------------------------
# ----------------- Magic Methods --------------------------------------------------------
# ----------------------------------------------------------------------------------------

    def __init__(self, connection: socket.socket, logger: callable = print):
        self.sock = connection
        self.logger = logger


    def __repr__(self):

        srcIP, srcPort = self.sock.getsockname()
        try:    # If socket is a client before connect or server than we have no endpoint
            destIP, destPort = self.sock.getpeername()
            return f"Connection from {srcIP}:{srcPort} to {destIP}:{destPort}"
        except:
            return f"A-Connection from {srcIP}:{srcPort}"
        
    
    def __enter__(self):
        self.logger("-----> Entered Connection class")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
        self.logger("-----> Existed Connection class")
# ------------------------------------------------------------------------------------------
# ----------------- Private Methods --------------------------------------------------------
# ------------------------------------------------------------------------------------------
    @staticmethod
    def __pack_message(message: str) -> bytes:
        msg_header = struct.pack("<I", len(message))
        return msg_header + message.encode()
    
    """
    @Pre: socket is open
    """
    def __get_msg_header(self):
        msg_len = self.sock.recv(4)           # at the moment this is not n
        tup = struct.unpack("<I", msg_len)
        return tup
    

    def __is_closed(self) -> bool:
        try:
            # this will try to read bytes without blocking and also without removing them from buffer (peek only)
            data = self.sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False  # socket is open and reading from it would block
        except ConnectionResetError:
            return True  # socket was closed for some other reason
        except Exception as e:
            return False
        return False
    

# -----------------------------------------------------------------------------------------
# ----------------- Public Methods --------------------------------------------------------
# -----------------------------------------------------------------------------------------
        
    @classmethod
    def connect(cls, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return Connection(sock)
    

    def send_message(self, message: str):
        msg = Connection.__pack_message(message)
        self.sock.send(msg)


    def receive_message(self):
        if self.__is_closed():
            raise ConnectionError
        else:
            from_client = ''
            header = self.__get_msg_header()
            expected_msg_leg = header[0]
            while True:
                data = self.sock.recv(4096)    
                if not data:
                    break
                from_client += data.decode()
            if len(from_client) != expected_msg_leg:
                self.logger("Message read from client is in different length than the header value")
            return from_client

    
    def close(self):
        self.sock.close()
