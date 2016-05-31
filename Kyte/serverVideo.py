import socket
import numpy
import cv2

FRAME_WIDTH = 256
FRAME_HEIGHT = 192
FULL_FRAME_LENGTH = FRAME_HEIGHT * FRAME_WIDTH * 3


def collectPackage (frame_length, conn):
    FRAME_COMPLETE = False
    frame_length_to_receive = frame_length
    data_received = ''

    while FRAME_COMPLETE == False :
        data_received += conn.recv(frame_length_to_receive)
        frame_length_to_receive = frame_length - len(data_received)
        if frame_length_to_receive == 0:
            FRAME_COMPLETE = True

    return data_received


def displayVideo(data):
    # Convert the data from a string, to a numpy matrix.
    frame = numpy.fromstring(data, dtype=numpy.uint8)
    #print frame.size
    frame = numpy.reshape(frame, (FRAME_HEIGHT,FRAME_WIDTH,3))
    # Display the frame.
    cv2.imshow('Video Preview', frame)
    cv2.waitKey(60)
    # Reset the values after we've received the whole frame.

def startVideoServer() :

    print 'SERVER STARTED'
    VIDEO_PORT = 50051
    VIDEO_HOST = ''

    frame_length =  4096
    frames_received = 0
    received_frames = 0
    data = ''
    cv2.namedWindow('Video Preview')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((VIDEO_HOST, VIDEO_PORT))
    s.listen(1)
    conn, addr = s.accept()
    print 'Connected by', addr

    while True:

        data_received = collectPackage(frame_length,conn)

        if len(data_received) ==  frame_length:
            data += data_received
        else :
            #print 'pachet primit incorect'
            while len(data_received) != frame_length:
                data_received += '0'
            data += data_received

        frames_received += frame_length
        #if frames_received >  FULL_FRAME_LENGTH-frame_length:
        if frames_received ==  FULL_FRAME_LENGTH:
            displayVideo(data)
            frames_received = 0
            data = ''

    cv2.destroyAllWindows()
    conn.close()
