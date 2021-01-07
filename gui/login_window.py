from functools import partial
from tkinter import *
from tkinter import ttk

FRAME_BG = '#80c1ff'
HEIGHT = 960
WIDTH = 1366

class LoginWindow(Toplevel):
    def __init__(self,gui):
        Toplevel.__init__(self)
        self.title("Login")
        self.geometry("220x325")
        Label(self, text="Please enter login details:").pack()
        Label(self, text="").pack()
        Label(self, text="Username").pack()
        username = StringVar()
        username_login_entry = Entry(self, textvariable=username)
        username_login_entry.pack()
        Label(self, text="").pack()
        Label(self, text="Password").pack()
        password = StringVar()
        password__login_entry = Entry(self, textvariable=password, show='*')
        password__login_entry.pack()
        Label(self, text="").pack()
        validate_and_login = partial(self.validate_and_login, username.get, password.get)
        Button(self, text="Log In", width=10, height=1, command=validate_and_login).pack()

        reg_labelframe = ttk.Labelframe(self, text="OR")
        reg_labelframe.pack(ipadx=20, ipady=5)
        Button(reg_labelframe, text="Register", width=10, height=1, command=gui.create_reg_window).pack()



    #TODO: implement!
    def validate_and_login(self,get_username, get_password):
        print("username entered :", get_username())
        print("password entered :", get_password())

        self.destroy()
