from functools import partial
from tkinter import *
from tkinter import ttk

class LoginWindow(Toplevel):
    def __init__(self,gui,db_manager):
        Toplevel.__init__(self)
        self.title("Login")
        self.geometry("220x325")
        Label(self, text="Please enter login details:").pack()
        Label(self, text="").pack()
        Label(self, text="Email").pack()
        email = StringVar()
        username_login_entry = Entry(self, textvariable=email)
        username_login_entry.pack()
        Label(self, text="").pack()
        Label(self, text="Password").pack()
        password = StringVar()
        password__login_entry = Entry(self, textvariable=password, show='*')
        password__login_entry.pack()
        Label(self, text="").pack()
        validate_and_login = partial(self.validate_and_login, email.get, password.get,db_manager)
        Button(self, text="Log In", width=10, height=1, command=validate_and_login).pack()

        reg_labelframe = ttk.Labelframe(self, text="OR")
        reg_labelframe.pack(ipadx=20, ipady=5)
        Button(reg_labelframe, text="Register", width=10, height=1, command=gui.create_reg_window).pack()



    #TODO: implement!
    def validate_and_login(self, get_email, get_password, db_manager):
        print("username entered :", get_email())
        print("password entered :", get_password())
        #TODO: popup if error
        isSuc,err=db_manager.logInUser(get_email(),get_password())

        self.destroy()
