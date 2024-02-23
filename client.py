
import socket
import cv2
import pickle
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "127.0.1.1"
port = 9994
client_socket.connect((host_ip, port))
data = b""
payload_size = struct.calcsize("Q")
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024)
        if not packet:
            break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4*1024)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    try:
        frame = pickle.loads(frame_data)
        cv2.imshow("Received", frame)
    except Exception as e:
        print(f"Error deserializing frame data: {e}")
        break

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

client_socket.close()
