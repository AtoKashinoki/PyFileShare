

import socket
from PyFileShare import share_directory

if __name__ == '__main__':
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    share_directory("../src/", host=str(host_ip))
    ...
