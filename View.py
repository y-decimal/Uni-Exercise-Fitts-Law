import tkinter as tk
from tkinter import ttk
import random

class View(ttk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        


    def run(self):
        
        self.draw_circle(1000, 1000, 50, "red")
        self.draw_random_circle()    
     
        
    def draw_circle(self, x, y, r, color):
        '''Draws a circle on the canvas'''
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline=color)
    
    def draw_random_circle(self):
        '''Draws a random circle on the canvas'''
        x = random.randint(0, self.canvas.winfo_width())
        y = random.randint(0, self.canvas.winfo_height())
        r = random.randint(10, 50)
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        self.draw_circle(x, y, r, color)