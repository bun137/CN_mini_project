import socket
import cv2
import pickle
import struct
import imutils
import threading


def handle_client(client_socket):
    vid = cv2.VideoCapture(0)
    while True:
        ret, frame = vid.read()
        if not ret:
            break  # Break the loop if the video capture fails
        frame = imutils.resize(frame, width=320)
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        client_socket.sendall(message)

        cv2.imshow('Sending...', frame)
        key = cv2.waitKey(10) & 0xFF  # Handle key presses correctly
        if key == 13:  # ASCII value for enter key
            break
    vid.release()  # Release the VideoCapture resource
    cv2.destroyAllWindows()  # Close all OpenCV windows
    client_socket.close()  # Close the client socket


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '10.1.18.32'
port = 10051
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen(5)
print("Listening at:", socket_address)

try:
    while True:
        client_socket, addr = server_socket.accept()
        print("Connection from:", addr)
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket,))
        client_thread.start()
except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    server_socket.close()
