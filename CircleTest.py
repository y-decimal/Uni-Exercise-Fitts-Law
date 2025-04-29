import customtkinter as ctk
import random
import math

class App(ctk.CTkFrame):
    
    def __init__(self, root):
        
        super().__init__(root)
        self.root = root
        
        relative_size = 0.75
        aspect_ratio = 16/9
        minimum_size = 0.2
        title = "Fitts Law Test"
        color = "#1e1e1e"
        
        self.circle1 = None
        self.circle2 = None
        
        self.radius = 25
        self.distance = 100
        
        self.set_window_parameters(relative_size, aspect_ratio, minimum_size, title)
        self.pack(fill="both", expand=True)
        
        self.canvas = ctk.CTkCanvas(self, background=color)
        self.canvas.pack(fill="both", expand=True)
        
        self.button = ctk.CTkButton(self, text="Generate Circle Pair", command=self.random_circle)
        self.button.pack(pady=10)
          
    def set_window_parameters(self, relative_size=0.5, aspect_ratio=16/9, minimum_size=0.2, title = "Test"):
        '''Sets window title, window size and aspect ratio'''

        # get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # set the window size relative to the screen size
        self.window_height = int(screen_height*relative_size)
        self.window_width = int(self.window_height*aspect_ratio)

        # find the center point of the screen
        center_x = int(screen_width/2 - self.window_width/2)
        center_y = int(screen_height/2 - self.window_height/2)

        # set the position of the window to the center of the screen
        self.root.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

        # set the minimum size of the window
        minimum_height = int(screen_height*minimum_size)
        minimum_width = int(minimum_height*aspect_ratio)
        self.root.minsize(minimum_width, minimum_height)

        # set the title of the window
        self.root.title(title)   
        
    def random_circle(self):
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        border_width = 150
        border_bottom = 0 + border_width
        border_right = width - border_width
        border_left = 0 + border_width
        border_top = height - border_width
        
        self.canvas.create_line(border_left, border_bottom, border_left, border_top, fill="grey", width=2)
        self.canvas.create_line(border_left, border_bottom, border_right, border_bottom, fill="grey", width=2)
        self.canvas.create_line(border_right, border_bottom, border_right, border_top, fill="grey", width=2)
        self.canvas.create_line(border_left, border_top, border_right, border_top, fill="grey", width=2)
        
        r = self.radius
        x1 = random.randint(border_left+r, border_right-r) 
        y1 = random.randint(border_bottom+r, border_top-r)
        
        self.canvas.delete(self.circle1)    
        self.circle1 = self.canvas.create_aa_circle(x1, y1, r, fill="red")    

  
        def generate_circle_2(x1, y1, r): 
            theta = random.uniform(0, 2*math.pi)
            x2 = int (x1 + (self.distance+2*r) * math.cos(theta))
            y2 = int (y1 + (self.distance+2*r) * math.sin(theta))
            # print (f"X2: {x2}, Y2: {y2}, True Distance: {math.sqrt((x2-x1)**2 + (y2-y1)**2)}, Distance: {self.distance}, Radius: {r}")
            self.canvas.delete(self.circle2)
            self.circle2 = self.canvas.create_aa_circle(x2, y2, r, fill="green")
            return x2, y2
        
        x2, y2 = generate_circle_2(x1, y1, r)
        # while (x2-r < border_left or x2+r > border_right or y2-r < border_bottom or y2+r > border_top):
        #     x2, y2 = generate_circle_2(x1, y1, r)
        #     print ("Regenerate Circle 2")
           



        
        
if __name__ == "__main__":
    
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
