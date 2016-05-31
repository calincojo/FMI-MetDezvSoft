import socket
import numpy
import cv2
import serverVideo
import clientAudio
import threading
import time

def videoClient(IP) :
    HOST = IP   # The remote host
    VIDEO_PORT = 50051  # The same port as used by the server

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, VIDEO_PORT))

    capture = cv2.VideoCapture(0)
    capture.open(0)

    print 'Starting data transmission...'

    frames_sent = 0
    full_frame_length = 147456
    frame_length = 4096
    frame_width = 256
    frame_height = 192

    print("*recording")

    ret = True
    while (capture.isOpened()):

        if ret == True:

            ret, frame_640x480 = capture.read()
            frame = cv2.resize(frame_640x480, (frame_width, frame_height))

            #cv2.imshow('Video Preview', frame)
            cv2.waitKey(60)

            frame = frame.flatten()
            data = frame.tostring()

            if ret:
                length_of_data = len(data)
                eaten_data = 0

                while (eaten_data + frame_length) <= length_of_data:
                    data_chunk = data[eaten_data:eaten_data + frame_length]
                    eaten_data += frame_length
                    s.sendall(data_chunk)
                frames_sent += 1

    print("*done recording")

    capture.release()
    cv2.destroyAllWindows()
    s.close()

    print("*closed")
