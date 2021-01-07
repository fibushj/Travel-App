from tkinter import *

FRAME_BG = '#80c1ff'
HEIGHT = 960
WIDTH = 1366

class StatisticsWindow(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Statistics")
        self.geometry("210x250")