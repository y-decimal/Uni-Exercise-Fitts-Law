import customtkinter as ctk
import random
import math
import time

class App(ctk.CTkFrame):
    
    def __init__(self, root):
        
        super().__init__(root)
        self.root = root
        
        relative_size = 0.75
        aspect_ratio = 16/9
        minimum_size = 0.2
        title = "Fitts Law Test"
        color = "#1e1e1e"
        
        self.set_window_parameters(relative_size, aspect_ratio, minimum_size, title)
        self.pack(fill="both", expand=True)
        
        self.results = []
        self.csv_file = "resultsMouse.csv"
        
        self.current_circle1, self.current_circle2 = None, None
        self.prev_circle1, self.prev_circle2 = None, None
        self.last_clicked_circle = None
        self.radius = 25
        self.distance = 100
        self.iteration = 0
        self.click_count = 0
        self.canvas = ctk.CTkCanvas(self, background=color)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.tag_bind("Circle1", "<Button-1>", lambda event: self.update_circle(self.current_circle1))   
        self.canvas.tag_bind("Circle2", "<Button-1>", lambda event: self.update_circle(self.current_circle2)) 
        self.canvas.tag_bind("Circle1", "<Enter>", lambda event: self.canvas.itemconfig(self.current_circle1, fill="green"))
        self.canvas.tag_bind("Circle1", "<Leave>", lambda event: self.canvas.itemconfig(self.current_circle1, fill="red"))
        self.canvas.tag_bind("Circle2", "<Enter>", lambda event: self.canvas.itemconfig(self.current_circle2, fill="green"))
        self.canvas.tag_bind("Circle2", "<Leave>", lambda event: self.canvas.itemconfig(self.current_circle2, fill="red"))
        # self.canvas.tag_bind("CircleClicked", "<Button-1>", self.clicked_circle)
        
        self.selector = ctk.CTkSegmentedButton(self, values=["Mouse", "VR"])
        self.selector.pack(pady=10)
        self.selector.set("Mouse")
        self.button = ctk.CTkButton(self, text="Start", command=self.start)
        self.button.pack(pady=10)
    
    def start(self):
        self.button.configure(state="disabled", text ="Running...")
        self.selector.configure(state="disabled")
        if self.selector.get() == "Mouse":
            self.csv_file = "resultsMouse.csv"
        else:
            self.csv_file = "resultsVR.csv"
        self.draw_random_circle()
    
    def update_circle(self, circle):
        self.canvas.delete(circle)
        self.click_count += 1
        if self.click_count == 2:
            self.end_time = time.perf_counter()
            self.time_taken = self.end_time - self.start_time
            print(f"Time taken: {self.time_taken:.5f} seconds")
            index_of_diff = self.calculate_index_of_difficulty(self.radius, self.distance)
            self.results.append((self.radius, self.distance, index_of_diff, self.time_taken))
            self.click_count = 0
            self.draw_random_circle()

        else:   
            self.start_time = time.perf_counter()
            
    def draw_random_circle(self, event=None):
        '''Draws a random circle on the canvas'''
        
        if (self.iteration == 27):
            self.canvas.delete(self.current_circle1)
            self.canvas.delete(self.current_circle2)
            self.button.configure(state="normal", text = "Save", command=self.save)
            self.button.pack(pady=10)
            return

        self.prev_circle1 = self.current_circle1
        self.prev_circle2 = self.current_circle2
        color = "red"
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if (self.iteration % 3 == 0):
            self.radius += 25
            print(f"Iteration: {self.iteration}, Radius: {self.radius}")
            
        if (self.iteration % 9 == 0):
            self.distance += 200
            self.radius = 25
            print(f"Iteration: {self.iteration}, Distance: {self.distance}")
        
        r = self.radius
        x1 = random.randint(0+r, width-r) 
        y1 = random.randint(0+r, height-r)
        
        # print (f"X1: {x1}, Y1: {y1}, Radius: {r}")
  
        def generate_circle_2(x1, y1, r): 
            theta = random.uniform(0, 2*math.pi)
            x2 = int (x1 + (self.distance+2*r) * math.cos(theta))
            y2 = int (y1 + (self.distance+2*r) * math.sin(theta))
            # print (f"X2: {x2}, Y2: {y2}, True Distance: {math.sqrt((x2-x1)**2 + (y2-y1)**2)}, Distance: {self.distance}, Radius: {r}")
            return x2, y2
        
        x2, y2 = generate_circle_2(x1, y1, r)
        while (x2-r < 0 or x2+r > width or y2-r < 0 or y2+r > height):
            x2, y2 = generate_circle_2(x1, y1, r)
           

        self.canvas.delete(self.prev_circle1)
        self.canvas.delete(self.prev_circle2)
        
        self.current_circle1 = self.canvas.create_aa_circle(x1, y1, r, fill=color, tags=("Circle1"))
        self.current_circle2 = self.canvas.create_aa_circle(x2, y2, r, fill=color, tags=("Circle2"))

        self.iteration += 1
        
    def calculate_index_of_difficulty(self, radius, distance):
        '''Calculates the index of difficulty using Fitts' Law'''
        # ID = log2(distance/radius + 1)
        # return ID
        return math.log2((distance / radius) +1)    
        
    def save(self):
        with open(self.csv_file, "w") as logfile:
            header = "Radius,Distance,Index of Difficulty,Time Taken\n"
            logfile.write(header)
            for result in self.results:
                logfile.write(f"{result[0]},{result[1]},{result[2]},{result[3]}\n")
        print(f"Results saved to {self.csv_file}")
        self.root.quit()

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
           
    def update_window_height(self, *args):
        '''Updates the window height and width'''
    
        self.prev_window_height = self.window_height
        self.prev_window_width = self.window_width
        
        self.window_height = self.root.winfo_height()
        self.window_width = self.root.winfo_width()
        
        # if self.prev_window_height != self.window_height and self.prev_window_width != self.window_width:
        #     self.update_canvas
        
    def get_window_size(self):
        '''Returns the window size'''
        return self.winfo_width(), self.winfo_height()
        
if __name__ == "__main__":
    
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
