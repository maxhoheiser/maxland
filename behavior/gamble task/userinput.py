import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import tkinter.font as font


# To Do
# move from setting to task setting object
# update object settings directly

class UserInput():
    def __init__(self, settings):
        self.settings = settings
        self.root = tk.Tk()
        geometry_string = self.get_geometry()
        self.root.title("Maxland")
        self.root.geometry(geometry_string)
        self.fontStyleBold = font.Font(family="Calibri", size=20)
        self.fontStyleRegular = font.Font(family="Calibri", size=12)
        # controlle variables for user input
        self.check_waight = False

    def get_geometry(self):
        WINDOW_SIZE = [800, 1000]
        screen_size = [self.root.winfo_screenwidth(), self.root.winfo_screenheight()]
        window_offset = [ int((screen_size[0]-WINDOW_SIZE[0])/2),
                          int((screen_size[1]-WINDOW_SIZE[1])/2)
                        ]
        if WINDOW_SIZE[0] > screen_size[0]:
            WINDOW_SIZE[0] = screen_size[0]
            window_offset[0] = 0
        if WINDOW_SIZE[1] > screen_size[1]:
            WINDOW_SIZE[1] = screen_size[1]
            window_offset[1] = 0
        return str(WINDOW_SIZE[0]) + "x" + str(WINDOW_SIZE[1]) + "+" + str(window_offset[0]) + "+" + str(window_offset[1])

    # grafical elements        
    def ok_button(self):
        self.settings.gamble_side = str(self.var_gamble_side.get()) 
        # check if animal waight is put in correctly
        if len(self.etr_animal_waight.get()) != 0 and self.is_float(self.etr_animal_waight.get()):
            self.check_waight = True
            self.settings.animal_waight = float(self.etr_animal_waight.get())
        elif len(self.etr_animal_waight.get()) == 0:
            messagebox.showwarning("Warning","Please input animal waight")
        else:
            messagebox.showwarning("Warning","Animal waight must be a float or integer")
        self.close()

    # def horizontal_line(self):
    #     # draw horizontal line
    #     h_line = tk.Canvas(self.root,  ) 

    def draw_window(self):
        # frame heading =================
        frame_heading = tk.Frame(master=self.root).pack()
        # heading
        lbl_main_title = tk.Label(self.root, text="Gamble Task Settings", font=self.fontStyleBold).pack()
        lbl_sub_title = tk.Label(self.root, text="plese set session settings and press OK", font=self.fontStyleRegular).pack()

        # frame essential input =================        
        # gamble side selction
        self.var_gamble_side = tk.StringVar(self.root)
        self.var_gamble_side.set(self.settings.gamble_side)
        dd_gamble_side = tk.OptionMenu(self.root, self.var_gamble_side, "Left", "Right").pack()
        # animal waight input
        lbl_animal_waight =  tk.Label(self.root, text="Animal waight", font=self.fontStyleRegular).pack()#grid(row=0)
        self.etr_animal_waight = tk.Entry(self.root)
        self.etr_animal_waight.pack()#grid(row=0, column=1)
        
        # frame trial blocks =================
        # blocks
        
        # frame rewards =================
        # reward small
        
        # reward big
        
        
        
        # frame times =================
        

        # frame stimulus =================

        

        # ok button
        button = tk.Button(self.root, text="OK", command=self.ok_button)
        button.pack()



    def show_window(self):    
        self.root.mainloop()
        
    def close(self):
        if self.check_waight:
            self.root.destroy()
        
    # helper funcitons
    def is_float(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False        