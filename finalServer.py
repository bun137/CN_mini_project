

import socket
import cv2
import pickle
import struct
import threading


vid = cv2.VideoCapture(0)


def handle_client(client_socket):
    print("GOT CONNECTION FROM:", client_socket.getpeername())
    try:
        while vid.isOpened():
            img, frame = vid.read()
            if img:
                data = pickle.dumps(frame)
                message = struct.pack("Q", len(data)) + data
                client_socket.sendall(message)
            else:
                break
    finally:
        client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host_name = socket.gethostname()
    host_ip = '192.168.1.18'
    print('HOST IP:', host_ip)
    port = 9995
    socket_address = (host_ip, port)

    server_socket.bind(socket_address)
    server_socket.listen(5)
    print("LISTENING AT:", socket_address)

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    main()
