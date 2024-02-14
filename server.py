import socket
import cv2
import pickle
import struct
import imutils

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = '10.1.18.32'
print('HOST IP:', host_ip)
port = 10050
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen(5)
print("Listening at:", socket_address)
while True:
    client_socket, addr = server_socket.accept()
    print("conection from:", addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        while (vid.isOpened()):
            img, frame = vid.read()
            frame = imutils.resize(frame, width=320)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)

            cv2.imshow('Sending...', frame)
            key = cv2.waitKey(10)
            if key == 13:
                client_socket.close()
                break
