from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from random import randint
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class PieGraph:
    def __init__(self,parent_frame):

        new_york = float("100")
        paris = float("80")
        london = float("60")
        titan = float("40")
        brooklyn = float("20")

        self.figure2 = Figure(figsize=(4.2,4), dpi=100)
        self.subplot2 = self.figure2.add_subplot(111)
        self.labels2 = 'New York', 'Paris', 'London', 'Titan', 'Brooklyn'
        self.pieSizes = [float(new_york),float(paris),float(london),float(titan), float(brooklyn)]
        self.explode2 = (0, 0, 0, 0, 0)
        self.subplot2.pie(self.pieSizes, explode=self.explode2, labels=self.labels2, autopct='%1.1f%%', shadow=True, startangle=90)
        self.subplot2.axis('equal')
        self.pie2 = FigureCanvasTkAgg(self.figure2, parent_frame)
        self.pie2.get_tk_widget().pack(anchor=tk.E)

    # def update(self):
    #     num = [float(randint(30,100)) for _ in range(5)]
    #     self.subplot2.clear()
    #     self.subplot2.pie(num, explode=self.explode2, labels=self.labels2, autopct='%1.1f%%', shadow=True, startangle=90)
    #     self.pie2.draw_idle()
    #     window.after(1000, self.update)