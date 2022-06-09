import select, socket, os, shutil
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import threading, wave, pyaudio, pickle, struct
import subprocess
from subprocess import call
from pytube import YouTube
from pydub import AudioSegment
import mysql.connector
import atexit
import bcrypt

from Server import Server
from Client import Client

class ISS:

    def __init__(self,IP,port):
        self.IP = IP
        self.port = port
        #self.ISS = self.Opening_Page()
        #self.ISS = self.start()
        #self.shown = True
        self.window = Tk()
        self.Opening_Page()
        self.window.geometry("1000x600")
        self.window.configure(bg="#ffffff")
        self.window.resizable(False, False)
        self.window.mainloop()

    def Opening_Page(self):
        canvas = Canvas(
            self.window,
            bg="#ffffff",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge")

        canvas.place(x=0, y=0)

        img0 = PhotoImage(file=f"img0_opening.png")
        b0 = Button(
            image=img0,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.Button_Opening(0),
            relief="flat")
        b0.image = img0

        b0.place(
            x=602, y=440,
            width=308,
            height=50)

        background_img = PhotoImage(file=f"background_opening.png")
        background = canvas.create_image(
            484.5, 300.0,
            image=background_img)
        canvas.image = background_img

        img1 = PhotoImage(file=f"img1_opening.png")
        b1 = Button(
            image=img1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.Button_Opening(1),
            relief="flat")
        b1.image = img1

        b1.place(
            x=602, y=367,
            width=308,
            height=49)


    def Button_Opening(self,button_id):
        if button_id == 0:
            self.SignUp_Page()
        else:
            self.Login_Page()

    def Login_Page(self):
        canvas = Canvas(
            self.window,
            bg="#ffffff",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        canvas.place(x=0, y=0)

        background_img = PhotoImage(
            file=f"background_login.png")
        background = canvas.create_image(
            553.0, 300.0,
            image=background_img)
        canvas.image = background_img

        entry0_img = PhotoImage(
            file=f"img_textBox0_login.png")
        entry0_bg = canvas.create_image(
            302.5, 277.5,
            image=entry0_img)

        entry0 = Entry(
            bd=0,
            bg="#197db5",
            highlightthickness=0)

        entry0.place(
            x=145.5, y=255,
            width=314.0,
            height=43)
        entry0.image = entry0_img

        entry1_img = PhotoImage(
            file=f"img_textBox1_login.png")
        entry1_bg = canvas.create_image(
            300.5, 375.5,
            image=entry1_img)

        entry1 = Entry(
            bd=0,
            bg="#197db5",
            highlightthickness=0)

        entry1.place(
            x=143.5, y=353,
            width=314.0,
            height=43)
        entry1.image = entry1_img

        img0 = PhotoImage(file=f"img0_login.png")
        b0 = Button(
            image=img0,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.Button_Login(entry0.get(), entry1.get()),
            relief="flat")

        b0.place(
            x=231, y=456,
            width=143,
            height=58)
        b0.image = img0

        img1 = PhotoImage(file=f"img1_Return_Opening.png")
        b1 = Button(
            image=img1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.Opening_Page(),
            relief="flat")

        b1.place(
            x=5, y=5,
            width=48,
            height=48)
        b1.image = img1

    def Button_Login(self, username, password):
        mydb = mysql.connector.connect(host="localhost",
                                       user="root",
                                       passwd="root",
                                       database="mydatabase"
                                       )

        mycursor = mydb.cursor()
       # mycursor.execute("DROP TABLE users")
        try:
            get_password = mycursor.execute("SELECT password FROM users WHERE username = %s", (username,))
            user_password = mycursor.fetchall()
            user_password = user_password[0][0]

            if bcrypt.checkpw(password.encode('utf-8'), bytes(user_password).rstrip(b'\x00')):
                try:
                    get_main = mycursor.execute("SELECT main FROM users WHERE username =%s", (username,))
                    main = mycursor.fetchall()
                    main = main[0][0]

                    mycursor.execute("SELECT * FROM users")
                    myresult = mycursor.fetchall()
                    for x in myresult:
                        print(x)
                    print("main ", main)

                    if main == "yes":
                        mycursor.execute("UPDATE users SET main ='no' WHERE username =%s", (username,))
                        mydb.commit()
                        self.Main_Options(username),
                    else:
                        self.Secondary_PC(username)

                except:
                    mycursor.execute("UPDATE users SET main ='yes' WHERE username =%s", (username,))
                    mydb.commit()

                    self.Main_Options(username),

            else:
                print("login")
                messagebox.showinfo("", "wrong input, try again")

        except:
             print("wrong")
             messagebox.showinfo("", "wrong input, try again")

    def Secondary_PC(self,client_username):
        print("secon")
        self.window.destroy()
        client = Client(self.IP,self.port,client_username)


    def SignUp_Page(self):
        canvas = Canvas(
            self.window,
            bg="#ffffff",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        canvas.place(x=0, y=0)

        background_img = PhotoImage(
            file=f"background_signup.png")
        background = canvas.create_image(
            510.5, 293.5,
            image=background_img)
        canvas.image = background_img

        entry0_img = PhotoImage(
            file=f"img_textBox0_signup.png")
        entry0_bg = canvas.create_image(
            279.0, 226.0,
            image=entry0_img)

        entry0 = Entry(
            bd=0,
            bg="#197db5",
            highlightthickness=0)

        entry0.place(
            x=139.0, y=203,
            width=280.0,
            height=44)
        entry0.image = entry0_img

        entry1_img = PhotoImage(
            file=f"img_textBox1_signup.png")
        entry1_bg = canvas.create_image(
            282.0, 317.0,
            image=entry1_img)

        entry1 = Entry(
            bd=0,
            bg="#197db5",
            highlightthickness=0)

        entry1.place(
            x=142.0, y=294,
            width=280.0,
            height=44)
        entry1.image = entry1_img

        entry2_img = PhotoImage(
            file=f"img_textBox2_signup.png")
        entry2_bg = canvas.create_image(
            282.0, 408.0,
            image=entry2_img)

        entry2 = Entry(
            bd=0,
            bg="#197db5",
            highlightthickness=0)

        entry2.place(
            x=142.0, y=385,
            width=280.0,
            height=44)
        entry2.image = entry2_img

        img0 = PhotoImage(file=f"img0_signup.png")
        b0 = Button(
            image=img0,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.Button_SignUp(entry0.get(), entry1.get(), entry2.get()),
            relief="flat")

        b0.place(
            x=210, y=455,
            width=138,
            height=83)
        b0.image = img0

        img1 = PhotoImage(file=f"img1_Return_Opening.png")
        b1 = Button(
            image=img1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:self.Opening_Page(),
            relief="flat")

        b1.place(
            x=5, y=5,
            width=48,
            height=48)
        b1.image = img1

    def Button_SignUp(self, username, password, confirm_password):

        if not str(username).isalnum():
            messagebox.showinfo(",", "Invalid request, username must contain only letters and numbers")
        elif password != confirm_password:
            messagebox.showinfo("", "password and confrim password are not identical")
        elif not password or not confirm_password:
            messagebox.showinfo("", "pleasd fill the blanks")
        else:
            mydb = mysql.connector.connect(host="localhost",
                                           user="root",
                                           passwd="root",
                                           database="mydatabase"
                                           )

            mycursor = mydb.cursor()
            #mycursor.execute("CREATE DATABASE mydatabse")
            mycursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255), password VARBINARY(255), main VARCHAR(255))")
            get_name = mycursor.execute("SELECT username FROM users WHERE username =%s", (username,))
            name = mycursor.fetchall()
            if len(name) == 0 :
                sql = "INSERT INTO users (username, password, main) VALUES (%s, %s, %s)"
                val = (username, bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()), "yes")
                mycursor.execute(sql, val)
                mydb.commit()
                messagebox.showinfo("", "Welcome " + username + " ! you have been added to the system")
                self.Login_Page()
            else:
                messagebox.showinfo("", "Username has been taken already")

    def Main_Options(self,username):
        canvas = Canvas(
            self.window,
            bg="#ffffff",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        canvas.place(x=0, y=0)

        background_img = PhotoImage(
            file=f"background_option.png")
        background = canvas.create_image(
            500.0, 300.0,
            image=background_img)
        canvas.image = background_img

        img0 = PhotoImage(file=f"img0_option_play.png")
        b0 = Button(
            image=img0,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.Button_Option(0,username),
            relief="flat")

        b0.place(
            x=341, y=309,
            width=312,
            height=50)
        b0.image = img0

        img1 = PhotoImage(file=f"img1_option_download.png")
        b1 = Button(
            image=img1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.Button_Option(1,username),
            relief="flat")

        b1.place(
            x=344, y=392,
            width=312,
            height=50)
        b1.image = img1

    def Button_Option(self,button_id,username):
        if button_id == 0:
            file_path = filedialog.askopenfilename(initialdir="Songs_library", title="Your Song Library")
            file_name = os.path.basename(file_path)
            print("first: ", file_name)
            if len(file_path)>0:
                self.PC_Number(file_path,file_name,username)
            else:
                self.Main_Options(username)
        else:
            self.Download_Song(username)

    def PC_Number(self,file_path,file_name,username):
        canvas = Canvas(
            self.window,
            bg="#ffffff",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        canvas.place(x=0, y=0)

        background_img = PhotoImage(
            file=f"background_number.png")
        background = canvas.create_image(
            500.0, 298.0,
            image=background_img)
        canvas.image = background_img

        entry0_img = PhotoImage(
            file=f"img_textBox0_number.png")
        entry0_bg = canvas.create_image(
            499.5, 421.5,
            image=entry0_img)

        entry0 = Entry(
            bd=0,
            bg="#ffffff",
            highlightthickness=0)

        entry0.place(
            x=357.5, y=396,
            width=284.0,
            height=49)
        entry0.image = entry0_img

        img0 = PhotoImage(file=f"img0_number.png")
        b0 = Button(
            image=img0,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.Button_PCNumber(file_path,entry0.get(),file_name,username),
            relief="flat")

        b0.place(
            x=444, y=481,
            width=112,
            height=37)
        b0.image = img0

        img1 = PhotoImage(file=f"img1_number_return.png")
        b1 = Button(
            image=img1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:self.Main_Options(username),
            relief="flat")

        b1.place(
            x=10, y=10,
            width=48,
            height=48)
        b1.image = img1

    def Button_PCNumber(self,file_path,PC_number,file_name,username):
        if PC_number.isdigit():
            messagebox.showinfo("", "Waiting for all the computers to connect")
            self.Play(file_path, PC_number,file_name,username)
        else:
            messagebox.showinfo("", "Error occurred, try again")


    def Play(self, file_path, PC_number,file_name,username):
        print(file_name)
        stereo_audio = AudioSegment.from_file(file_path, format="wav")
        mono_audios = stereo_audio.split_to_mono()
        right_path = file_path.replace(".wav","_mono_right.wav")
        right_path = right_path.replace("Songs","Mono")
        print(right_path)
        left_path = file_path.replace(".wav","_mono_left.wav")
        left_path = left_path.replace("Songs","Mono")
        print(left_path)
        mono_right = mono_audios[0].export(right_path, format="wav")
        mono_left = mono_audios[1].export(left_path, format="wav")

        server = Server(self.IP,self.port,file_path,right_path,left_path,PC_number,username,self.window)

    def Download_Song(self,username):
        canvas = Canvas(
            self.window,
            bg="#ffffff",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        canvas.place(x=0, y=0)

        background_img = PhotoImage(
            file=f"background_download.png")
        background = canvas.create_image(
            500.0, 300.0,
            image=background_img)
        canvas.image = background_img

        entry0_img = PhotoImage(
            file=f"img_textBox0_download.png")
        entry0_bg = canvas.create_image(
            500.0, 341.0,
            image=entry0_img)

        entry0 = Entry(
            bd=0,
            bg="#197db5",
            highlightthickness=0)

        entry0.place(
            x=251.0, y=325,
            width=498.0,
            height=30)
        entry0.image = entry0_img

        entry1_img = PhotoImage(
            file=f"img_textBox1_download.png")
        entry1_bg = canvas.create_image(
            500.0, 403.0,
            image=entry1_img)

        entry1 = Entry(
            bd=0,
            bg="#197db5",
            highlightthickness=0)

        entry1.place(
            x=251.0, y=387,
            width=498.0,
            height=30)
        entry1.image = entry1_img

        img0 = PhotoImage(file=f"img0_download.png")
        b0 = Button(
            image=img0,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.Button_Download(entry0.get(), entry1.get(),username),
            relief="flat")

        b0.place(
            x=440, y=479,
            width=120,
            height=32)
        b0.image = img0

        img1 = PhotoImage(file=f"img1_download_return.png")
        b1 = Button(
            image=img1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:self.Main_Options(username),
            relief="flat")

        b1.place(
            x=10, y=10,
            width=48,
            height=48)
        b1.image = img1

    def Button_Download(self, file_URL, file_name,username):
        try:
            # url input from user
            yt = YouTube(str(file_URL))
            video = yt.streams.filter(only_audio=True).first()
            destination = str("Songs_Library")

            # download the file
            out_file = video.download(output_path=destination)
            title = file_name
            # save the file
            base, ext = os.path.splitext(out_file)

            not_valid = ["/", "\\", "|", ":", "?", ">", "<", "*", '\r""']
            current_title = yt.title

            for i in not_valid:
                count = current_title.count(i)
                if i in current_title:
                    current_title = current_title.replace(i, "", count)

            base = base.replace(current_title, title)
            new_file = base + '.mp3'

            os.rename(out_file, new_file)
            # convert mp3 to wav file
            subprocess.call(['ffmpeg', '-i', new_file, "Songs_Library\\" + title + ".wav"])
            os.remove(new_file)
            messagebox.showinfo("", title + " has been successfully downloaded.")
            self.Main_Options(username)

        except:
            messagebox.showinfo("", "Error occurred, try again")


def main():
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print(host_ip)
    print(type(host_ip))
    print(host_ip)
    IP = '0.0.0.0'
    #IP = '10.100.102.29'
    print(IP)
    port = 1234

    Improvised_Sound_System = ISS(IP,port)

if __name__ == '__main__':
    main()
