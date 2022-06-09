import select, socket, os
from tkinter import *
import threading, wave, pyaudio, pickle, struct
from pytube import YouTube
from pydub import AudioSegment
from threading import Thread
# duration import: import contextlib
from pydub.playback import play
import mysql.connector

class Server:

    def __init__(self,IP,port,file_path,right_path,left_path,PC_number,server_username,window):
        self.IP = IP
        self.port = port
        self.file_path = file_path
        self.right_path = right_path
        self.left_path = left_path
        self.PC_number = PC_number
        self.server_username = server_username

        self.window = window
        self.Server = self.Execute_Server()

    def Window(self):
        print("server")
        canvas = Canvas(
            self.window,
            bg="#ffffff",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        canvas.place(x=0, y=0)

        self.window.after(10000, lambda: self.window.destroy())

        background_img = PhotoImage(file=f"background_play.png")
        background = canvas.create_image(
            500.0, 300.0,
            image=background_img)
        canvas.image = background_img

    def Execute_Server(self):

        if self.PC_number == "0":
            Thread(target=self.Window).start()
            Thread(target=self.Play_Song, args=(self.file_path,)).start()

        else:
            server_socket = socket.socket()
            server_socket.bind((self.IP, self.port - 1))
            server_socket.listen(5)
            print("Setting up server...")
            print("Listening for clients...")
            client_sockets = []
            messages_to_send = []
            connections = []
            client_counter = 0
            run = True

            print('server listening at', (self.IP, self.port - 1))

            while run:
                rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
                for current_socket in rlist:
                    if current_socket is server_socket:
                        connection, client_address = current_socket.accept()
                        print("New client joined!", client_address)

                        length = str(len(self.server_username))
                        zfill_length = length.zfill(4)
                        server_username = zfill_length + self.server_username
                        connection.send(server_username.encode())

                        length = connection.recv(4).decode()
                        same_user = connection.recv(int(length)).decode()
                        print(same_user, "yess")

                        print(same_user, type(same_user))

                        if same_user != "wrong":
                            client_sockets.append(connection)
                            client_counter = client_counter + 1

                    if client_counter == int(self.PC_number):
                        mydb = mysql.connector.connect(host="localhost",
                                                       user="root",
                                                       passwd="root",
                                                       database="mydatabase"
                                                       )

                        mycursor = mydb.cursor()
                        mycursor.execute("SELECT * FROM users")
                        myresult = mycursor.fetchall()

                        for x in myresult:
                            print(x)

                        print(self.server_username)
                        mycursor.execute("UPDATE users SET main ='yes' WHERE username =%s", (self.server_username,))
                        mydb.commit()

                        mycursor.execute("SELECT * FROM users")
                        myresult = mycursor.fetchall()

                        for x in myresult:
                            print(x)

                        Thread(target=self.Window).start()
                        Thread(target=self.Play, args=(client_sockets,current_socket,server_socket,self.right_path,self.left_path)).start()

                        run = False


    def Play(self, client_sockets, current_socket, server_socket, right_path, left_path):
        CHUNK = 1024
        wf = wave.open(self.file_path, 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=2,
                        rate=wf.getframerate(),
                        input=True,
                        frames_per_buffer=CHUNK)

        wf_right = wave.open(right_path, 'rb')
        p_right = pyaudio.PyAudio()

        stream_right = p_right.open(format=p_right.get_format_from_width(wf_right.getsampwidth()),
                                    channels=1,
                                    rate=wf_right.getframerate(),
                                    input=True,
                                    frames_per_buffer=CHUNK)

        wf_left = wave.open(left_path, 'rb')
        p_left = pyaudio.PyAudio()

        stream_left = p_left.open(format=p_left.get_format_from_width(wf_left.getsampwidth()),
                                  channels=1,
                                  rate=wf_left.getframerate(),
                                  input=True,
                                  frames_per_buffer=CHUNK)

        data = None
        data_right = None
        data_left = None
        right = True
        message = None
        pc_counter = 0

        for client_socket in client_sockets:
            length = str(len(self.PC_number))
            zfill_length = length.zfill(4)
            PC_number = zfill_length + self.PC_number
            client_socket.send(PC_number.encode())

            if pc_counter == (int(self.PC_number) - 1) / 2:
                full_channels = "2"
            else:
                full_channels = "1"

            length = str(len(full_channels))
            zfill_length = length.zfill(4)
            channels = zfill_length + full_channels
            client_socket.send(channels.encode())
            pc_counter = pc_counter + 1

        while len(str(data_right)) != 3 or len(str(data_left)) != 3:
            data = wf.readframes(CHUNK)
            a = pickle.dumps(data)
            message = struct.pack("Q", len(a)) + a

            data_right = wf_right.readframes(CHUNK)
            a_right = pickle.dumps(data_right)
            message_right = struct.pack("Q", len(a_right)) + a_right

            data_left = wf_left.readframes(CHUNK)
            a_left = pickle.dumps(data_left)
            message_left = struct.pack("Q", len(a_left)) + a_left

            if int(self.PC_number) % 2 == 0:
                for client_socket in client_sockets:
                    if right == True:
                        client_socket.sendall(message_right)
                        right = False
                    else:
                        client_socket.sendall(message_left)
                        right = True

            else:
                pc_counter = 0
                for client_socket in client_sockets:
                    if pc_counter < (int(self.PC_number) - 1)/ 2:
                        client_socket.sendall(message_right)
                    elif pc_counter == (int(self.PC_number) - 1)/2:
                        client_socket.sendall(message)
                    else:
                        client_socket.sendall(message_left)
                    pc_counter = pc_counter + 1
                    if pc_counter == int(self.PC_number):
                        pc_counter = 0

        print("Connection closed")
        for client_socket in client_sockets:
            client_sockets.remove(client_socket)

    def Play_Song(self,file_path):
        play_file = AudioSegment.from_file(file_path, format="wav")
        play(play_file)

        mydb = mysql.connector.connect(host="localhost",
                                       user="root",
                                       passwd="root",
                                       database="mydatabase"
                                       )

        mycursor = mydb.cursor()

        mycursor.execute("UPDATE users SET main ='yes' WHERE username =%s", (self.server_username,))
        mydb.commit()
