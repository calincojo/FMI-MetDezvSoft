__author__ = 'Cojocaru'
# Echo server program
import socket
import pyaudio
import wave
import time
import thread
import threading



def audioClient() :

    print 'Client Started'

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 1

    HOST = 'localhost'    # The remote host
    PORT = 50007               # The same port as used by the server

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("*recording")
    th = threading.Thread(group=None, target=sendAudio(s,stream,CHUNK), args=(), kwargs=())
    th.start()
    th.run()
   # t = thread.start_new_thread( sendAudio, (s,stream,CHUNK))
    audioServer()

    print("*done recording")
    time.sleep(10)

    stream.stop_stream()
    stream.close()
    p.terminate()
    s.close()

    print("*closed")




def sendAudio(socket,stream,CHUNK):

    frames = []

    while True :
      data  = stream.read(CHUNK)
      frames.append(data)
      socket.sendall(data)
  

def audioServer():

    print 'Server Started'

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 4
    #WAVE_OUTPUT_FILENAME = "server_output.wav"
    WIDTH = 2
    frames = []

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)


    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT =  50009                # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    f = s.makefile()
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print 'Connected by', addr
    data = conn.recv(1024)

    i=1
    while data != '':
        stream.write(data)
        data = conn.recv(1024)
       # frames.append(data)


    '''wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    '''
    stream.stop_stream()
    stream.close()
    p.terminate()
    conn.close()


#if __name__ == '__main__':
    #audioServer()