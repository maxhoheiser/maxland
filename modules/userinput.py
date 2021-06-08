import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
import tkinter.font as font
import os

# ToDo fix close button

class UserInput():
    def __init__(self, settings):
        """tkinter object to create user input window to update sessions parameter from preread userinputs file

        Args:
            settings (TrialPArameterHandler object): the object for all the session parameters from TrialPArameterHandler
        """
        self.settings = settings
        # setup tkinter variables
        self.root = tk.Tk()
        geometry_string = self.get_geometry()
        self.root.title("Maxland")
        self.root.geometry(geometry_string)
        self.fontStyleBold = font.Font(family="Calibri", size=20)
        self.fontStyleRegular = font.Font(family="Calibri", size=11)
        self.fontStyleBox = font.Font(family="Calibri", size=10)
        # controlle variables for user input
        self.check_weight = False
        self.padx = 30
        # catch close window press
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    # update settings variables
    def update_settings(self):
        """updates the settings object for the session with new values from userinput window

        Returns:
            settings (TrialParameterHandler object):  the object for all the session parameters from TrialPArameterHandler
        """
        self.settings.life_plot = bool(self.var_liveplot.get())
        self.settings.gamble_side = self.var_gamble_side.get()
        self.settings.blocks = self.get_blocks()
        self.settings.big_reward = float(self.var_big_reward.get())
        self.settings.small_reward = float(self.var_small_reward.get())
        # time dict
        self.settings.time_dict["time_start"] = float(self.time_start.var.get())
        self.settings.time_dict["time_wheel_stopping_check"] = float(self.time_wheel_stopping_check.var.get())
        self.settings.time_dict["time_wheel_stopping_punish"] = float(self.time_wheel_stopping_punish.var.get())
        self.settings.time_dict["time_stim_pres"] = float(self.time_stim_pres.var.get())
        self.settings.time_dict["time_open_loop"] = float(self.time_open_loop.var.get())
        self.settings.time_dict["time_open_loop_fail_punish"] = float(self.time_open_loop_fail_punish.var.get())
        self.settings.time_dict["time_stim_freez"] = float(self.time_stim_freez.var.get())
        self.settings.time_dict["time_reward"] = float(self.time_reward.var.get())
        self.settings.time_dict["time_inter_trial"] = float(self.time_inter_trial.var.get())
        self.settings.min_inter_trial_time()
        # ToDo update stimulus selected file from userintput
        #if 'stim_file' in locals():
        #    self.stim = str(self.stim_file)
        #self.settings.stim = self.btn_stim.
        self.settings.thresholds[0] = int(self.var_wheel_thresh_neg.get())
        self.settings.thresholds[1] = int(self.var_wheel_thresh_pos.get())
        self.settings.stim_end_pos = [int(self.var_stim_end_neg.get()), int(self.var_stim_end_pos.get())]
        self.settings.animal_weight = float(self.var_animal_weight.get())


    def update_settings_after(self):
        """updates the settings object from userinput from window after session"""
        self.settings.manual_reward = self.var_reward_manual.get()
        self.settings.animal_weight_after = self.var_animal_weight_after.get()
        self.settings.notes = self.notes.get("1.0", "end")



    # tkinter elements
    def get_geometry(self):
        """create tkinter window

        Returns:
            str: x y geometry of window
        """
        self.WINDOW_SIZE = [835, 920]
        screen_size = [self.root.winfo_screenwidth(), self.root.winfo_screenheight()]
        window_offset = [ int((screen_size[0]-self.WINDOW_SIZE[0])/2),
                          60
                        ]
        if self.WINDOW_SIZE[0] > screen_size[0]:
            self.WINDOW_SIZE[0] = screen_size[0]
            window_offset[0] = 0
        if self.WINDOW_SIZE[1] > screen_size[1]:
            self.WINDOW_SIZE[1] = screen_size[1]
            window_offset[1] = 0
        return str(self.WINDOW_SIZE[0]) + "x" + str(self.WINDOW_SIZE[1]) + "+" + str(window_offset[0]) + "+" + str(window_offset[1])


    # grafical elements
    def ok_button(self):
        """ok button on userinput window
        checks if animal weight was input valid and prompts warning if not
        """
        self.settings.gamble_side = str(self.var_gamble_side.get())
        # check if animal weight is put in correctly
        if len(self.var_animal_weight.get()) != 0 and self.is_float(self.var_animal_weight.get()):
            self.check_weight = True
            self.update_settings()
        elif len(self.var_animal_weight.get()) == 0:
            messagebox.showwarning("Warning","Please input animal weight")
        else:
            messagebox.showwarning("Warning","Animal weight must be a float or integer")
        self.close()

    def ok_button_after(self):
        """ok button for window after session, checks if animal weight after is input valid"""
        self.etr_animal_weight_after
        # check if animal weight is put in correctly
        if len(self.var_animal_weight_after.get()) != 0 and self.is_float(self.var_animal_weight_after.get()):
            self.update_settings_after()
        elif len(self.var_animal_weight_after.get()) == 0:
            messagebox.showwarning("Warning","Please input animal weight")
        else:
            messagebox.showwarning("Warning","Animal weight must be a float or integer")
        self.close()

    def cancle_button(self):
        self.close()


    #ToDo
    def file_dialog_button(self):
        """tkinter dialog for opening stimulus file from folder
        """
        stim_file = filedialog.askopenfilename(initialdir = "../../stimulus/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("png files","*.png")))


    def show_window(self):
        self.root.mainloop()


    def close(self):
        if self.check_weight:
            self.settings.run_session = True
            self.root.destroy()

        else:
            self.settings.run_session = False
            self.root.destroy()


    def is_float(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False


    def get_blocks(self):
        """update block variables for given block from userinput

        Args:
            block (dict): block dict with keys:
                trial_range_block (list): range of trial for given block
                prob_reward_gamble_block (float): probability for big reward
                prob_reward_save_block (float): probability for no reward block
        """
        block_list =[]
        for block in self.blocks:
            block_dict = {}
            block_dict["trial_range_block"] = [int(block.var_range_min.get()), int(block.var_range_max.get())]
            block_dict["prob_reward_gamble_block"] = float(block.var_prob_gb.get())
            block_dict["prob_reward_save_block"] = float(block.var_prob_save.get())
            block_list.append(block_dict)
        return block_list



    # Window Bevore ====================================================================
    def draw_window_bevore(self):
        """tkinter window to get user input, variables and default values are read from settings object
        """
        # heading
        lbl_main_title = tk.Label(self.root, text="Gamble Task Settings", font=self.fontStyleBold).pack()
        #lbl_sub_title = tk.Label(self.root, text="plese set session settings and press OK", font=self.fontStyleRegular).pack()

        # frame essential input
        lbl_essential = tk.Label(self.root, text="ESSENTIAL SETTINGS", font=self.fontStyleBox, fg='gray66').pack(anchor=tk.W, padx=self.padx-2)
        frame1 = tk.Frame(self.root, highlightbackground="black", highlightthickness=1)
        frame1.pack(fill=tk.BOTH, padx=self.padx, pady=(2,10))

        # gamble side selction
        lbl_gamble_side = tk.Label(frame1, text="Gamble Side:", font=self.fontStyleRegular)
        lbl_gamble_side.grid(row=0, column=0, padx=5, pady=8)
        self.var_gamble_side = tk.StringVar(frame1)
        self.var_gamble_side.set(self.settings.gamble_side)
        dd_gamble_side = tk.OptionMenu(frame1, self.var_gamble_side, "Left", "Right")
        dd_gamble_side.grid(row=0, column=1)

        # animal weight input
        lbl_animal_weight =  tk.Label(frame1, text="Animal weight:", font=self.fontStyleRegular)
        lbl_animal_weight.grid(row=0, column=3, padx=(20,5), pady=8)
        self.var_animal_weight = tk.StringVar(frame1)
        self.etr_animal_weight = tk.Entry(frame1, textvariable=self.var_animal_weight)
        self.etr_animal_weight.grid(row=0, column=4, pady=8)

        #live plotting
        self.var_liveplot = tk.IntVar(frame1, )
        self.var_liveplot.set(self.settings.life_plot)
        self.btn_liveplot = tk.Checkbutton(frame1, text="Life Plotting", variable=self.var_liveplot)
        self.btn_liveplot.grid(row=0, column=5, sticky='W', padx=20)

        # frame trial blocks ====================================================================
        # blocks
        lbl_block = tk.Label(self.root, text="BLOCKS", font=self.fontStyleBox, fg='gray66').pack(anchor=tk.W, padx=self.padx-2, pady=(10,2))
        frame2 = tk.Frame(self.root, highlightbackground="black", highlightthickness=1)
        frame2.pack(fill=tk.BOTH, padx=self.padx, pady=2)

        blk0 = self.Block(0, frame2, self.settings, self.fontStyleRegular, 0)
        blk1 = self.Block(1, frame2, self.settings, self.fontStyleRegular, 1)
        blk2 = self.Block(2, frame2, self.settings, self.fontStyleRegular, 2)

        self.blocks = [blk0, blk1, blk2]

        # frame rewards ====================================================================
        lbl_reward = tk.Label(self.root, text="REWARD", font=self.fontStyleBox, fg='gray66').pack(anchor=tk.W, padx=self.padx-2, pady=(15,2))
        frame3 = tk.Frame(self.root, highlightbackground="black", highlightthickness=1)
        frame3.pack(fill=tk.BOTH, padx=self.padx, pady=2)
        # reward big
        lbl_big_reward =  tk.Label(frame3, text="Gamble side reward [ml]:", font=self.fontStyleRegular)
        lbl_big_reward.grid(row=0, column=0, padx=5, pady=8)

        self.var_big_reward = tk.StringVar(frame3, value=self.settings.big_reward)
        self.etr_big_reward = tk.Entry(frame3, textvariable=self.var_big_reward, width=10)
        self.etr_big_reward.grid(row=0, column=1, pady=8)

        # reward small
        lbl_small_reward =  tk.Label(frame3, text="Save side reward [ml]:", font=self.fontStyleRegular)
        lbl_small_reward.grid(row=0, column=2, padx=(30,5), pady=8)

        self.var_small_reward = tk.StringVar(frame3, value=self.settings.small_reward)
        self.etr_small_reward = tk.Entry(frame3, textvariable=self.var_small_reward, width=10)
        self.etr_small_reward.grid(row=0, column=3, pady=8)

        # last time calibrated
        calib_text = "Last time calibrated: " + self.settings.last_callibration
        lbl_last_calib =  tk.Label(frame3, text=calib_text, font=self.fontStyleRegular)
        lbl_last_calib.grid(row=0, column=4, padx=(30,5), pady=8)


        # frame stimulus ====================================================================
        lbl_stimulus = tk.Label(self.root, text="STIMULUS", font=self.fontStyleBox, fg='gray66').pack(anchor=tk.W, padx=self.padx-2, pady=(15,2))
        frame4 = tk.Frame(self.root, highlightbackground="black", highlightthickness=1)
        frame4.pack(fill=tk.BOTH, padx=self.padx, pady=2)

        # frame row 0
        frame4_0 = tk.Frame(frame4)
        frame4_0.grid(row=0, column=0, sticky='W')
        # stimulus file
        lbl_stim_pos =  tk.Label(frame4_0, text="Stimulus File (jpeg, png):", font=self.fontStyleRegular)
        lbl_stim_pos.grid(row=0, column=0, padx=10, pady=8)

        #ToDo
        stimulus_name = self.settings.stim.split(os.sep)[-1]
        self.btn_stim = tk.Button(frame4_0, text=stimulus_name, command=self.file_dialog_button, width = 20)
        self.btn_stim.grid(row=0, column=1, pady=8)

        # frame row 1
        frame4_1 = tk.Frame(frame4)
        frame4_1.grid(row=1, column=0)
        # stimulus end position
        lbl_stim_pos =  tk.Label(frame4_1, text="Stim end pos [px]:", font=self.fontStyleRegular)
        lbl_stim_pos.grid(row=1, column=0, padx=(10,5), pady=8)

        self.var_stim_end_neg = tk.StringVar(frame4_1, value=self.settings.stim_end_pos[0])
        self.etr_stim_end_neg = tk.Entry(frame4_1, textvariable=self.var_stim_end_neg, width=6)
        self.etr_stim_end_neg.grid(row=1, column=1, padx=(0,2), pady=8, sticky='W')

        lbl_stim_til = tk.Label(frame4_1, text="to", font=self.fontStyleRegular)
        lbl_stim_til.grid(row=1, column=2, pady=8, sticky='W')

        self.var_stim_end_pos = tk.StringVar(frame4_1, value=self.settings.stim_end_pos[1])
        self.etr_stim_end_pos = tk.Entry(frame4_1, textvariable=self.var_stim_end_pos, width=6)
        self.etr_stim_end_pos.grid(row=1, column=3, padx=(2,10), pady=8, sticky='W')

        # # wheel rotation
        lbl_stim_pos =  tk.Label(frame4_1, text="Wheel threhsold [deg]:", font=self.fontStyleRegular)
        lbl_stim_pos.grid(row=1, column=4, padx=(10,5), pady=8)

        self.var_wheel_thresh_neg = tk.StringVar(frame4_1, value=self.settings.thresholds[0])
        self.etr_wheel_thresh_neg = tk.Entry(frame4_1, textvariable=self.var_wheel_thresh_neg, width=8)
        self.etr_wheel_thresh_neg.grid(row=1, column=5, padx=(0,2), pady=8, sticky='W')

        lbl_wheel_til = tk.Label(frame4_1, text="to", font=self.fontStyleRegular)
        lbl_wheel_til.grid(row=1, column=6, pady=8, sticky='W')

        self.var_wheel_thresh_pos = tk.StringVar(frame4_1, value=self.settings.thresholds[1])
        self.etr_wheel_thresh_pos = tk.Entry(frame4_1, textvariable=self.var_wheel_thresh_pos, width=8)
        self.etr_wheel_thresh_pos.grid(row=1, column=7, padx=(2,10), pady=8, sticky='W')

        # frame time ====================================================================
        lbl_time = tk.Label(self.root, text="TIME", font=self.fontStyleBox, fg='gray66').pack(anchor=tk.W, padx=self.padx-2, pady=(15,2))
        frame5 = tk.Frame(self.root, highlightbackground="black", highlightthickness=1)
        frame5.pack(fill=tk.BOTH, padx=self.padx, pady=2)

        frame5_0 = tk.Frame(frame5)
        frame5_0.grid(row=0, column=0, pady= 8, sticky='W')

        # row 0
        # create a new instance of object Time (defined below) with the parameters frame (werhe to place), fontstyle, name and default value
        # call the varaiable var from the instance to get the inputed value
        self.time_start = self.Time(frame5_0, 0, self.fontStyleRegular, "Start wait Time",
                                            self.settings.time_dict["time_start"],
                                            "time bevor the trial starts"
                                            )
        # row 1
        self.time_wheel_stopping_check = self.Time(frame5_0, 1, self.fontStyleRegular, "Stopping check",
                                            self.settings.time_dict["time_wheel_stopping_check"],
                                            "time the wheel has to be stopped"
                                            )
        # row 2
        self.time_wheel_stopping_punish = self.Time(frame5_0, 2, self.fontStyleRegular, "Not stpping punish",
                                               self.settings.time_dict["time_wheel_stopping_punish"],
                                               "time wait if the wheel is not stopped bevore new trial starts"
                                               )
        # row 3
        self.time_stim_pres = self.Time(frame5_0, 3, self.fontStyleRegular, "Stim Presentation",
                                   self.settings.time_dict["time_stim_pres"],
                                   "time stimulus is presented but not movable"
                                  )
        # row 4
        self.time_open_loop = self.Time(frame5_0, 4, self.fontStyleRegular, "Open Loop",
                                   self.settings.time_dict["time_open_loop"],
                                   "time of open loop where wheel moves the stimulus"
                                   )
        # row 5
        self.time_open_loop_fail_punish = self.Time(frame5_0, 5, self.fontStyleRegular, "Open Loop Fail",
                                   self.settings.time_dict["time_open_loop_fail_punish"],
                                   "time wait if stimulus not moved far enough to position"
                                   )
        # row 6
        self.time_stim_freez = self.Time(frame5_0, 6, self.fontStyleRegular, "Stim Freez",
                                   self.settings.time_dict["time_stim_freez"],
                                   "time stimulus is presented at reached position but not movable anymore"
                                   )
        # row 7
        self.time_reward = self.Time(frame5_0, 7, self.fontStyleRegular, "Reward Time",
                                   self.settings.time_dict["time_reward"],
                                   "time the animal has for the reard = valve open + time after"
                                   )
        # row 8
        self.time_inter_trial = self.Time(frame5_0, 8, self.fontStyleRegular, "Trial End",
                                   self.settings.time_dict["time_inter_trial"],
                                   "time at end of each Trial"
                                   )



        # ok button
        btn_ok = tk.Button(self.root, text="OK", command=self.ok_button, width = 20)
        btn_ok.pack(side=tk.RIGHT, padx=self.padx, pady=10)
        # cancle button
        btn_cancle = tk.Button(self.root, text="Cancel", command=self.cancle_button, width = 20)
        btn_cancle.pack(side=tk.RIGHT)


    # Window After ====================================================================
    def draw_window_after(self):
        """tkinter window to get user input after session, variables and default values are read from settings object
        """
        # heading
        lbl_main_title = tk.Label(self.root, text="Gamble Task Report", font=self.fontStyleBold).pack()
        #lbl_sub_title = tk.Label(self.root, text="plese set session settings and press OK", font=self.fontStyleRegular).pack()

        # frame essential input
        lbl_essential = tk.Label(self.root, text="ESSENTIAL SETTINGS", font=self.fontStyleBox, fg='gray66').pack(anchor=tk.W, padx=self.padx-2)
        frame1 = tk.Frame(self.root, highlightbackground="black", highlightthickness=1)
        frame1.pack(fill=tk.BOTH, padx=self.padx, pady=(2,10))

        # animal weight input
        lbl_animal_weight =  tk.Label(frame1, text="Animal weight after:", font=self.fontStyleRegular)
        lbl_animal_weight.grid(row=0, column=3, padx=(20,5), pady=8)
        self.var_animal_weight_after = tk.StringVar(frame1)
        self.etr_animal_weight_after = tk.Entry(frame1, textvariable=self.var_animal_weight_after)
        self.etr_animal_weight_after.grid(row=0, column=4, pady=8)


        # frame manual rewards ====================================================================
        lbl_reward = tk.Label(self.root, text="MANUAL REWARD", font=self.fontStyleBox, fg='gray66').pack(anchor=tk.W, padx=self.padx-2, pady=(15,2))
        frame3 = tk.Frame(self.root, highlightbackground="black", highlightthickness=1)
        frame3.pack(fill=tk.BOTH, padx=self.padx, pady=2)
        # reward big
        lbl_reward =  tk.Label(frame3, text="Manual administered reward [ml]:", font=self.fontStyleRegular)
        lbl_reward.grid(row=0, column=0, padx=5, pady=8)

        self.var_reward_manual = tk.StringVar(frame1)
        self.etr_reward_manual = tk.Entry(frame3, textvariable=self.var_reward_manual, width=10)
        self.etr_reward_manual.grid(row=0, column=1, pady=8)

        # frame time ====================================================================
        lbl_time = tk.Label(self.root, text="NOTES", font=self.fontStyleBox, fg='gray66').pack(anchor=tk.W, padx=self.padx-2, pady=(15,2))

        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.notes = tk.Text(self.root, highlightbackground="black", highlightthickness=1, height=38, width=10)
        self.notes.pack(fill=tk.BOTH, padx=self.padx, pady=2)

        scrollbar.config(command=self.notes.yview)
        self.notes.config(yscrollcommand=scrollbar.set)


        # ok button
        btn_ok = tk.Button(self.root, text="OK", command=self.ok_button_after, width = 20)
        btn_ok.pack(side=tk.RIGHT, padx=self.padx, pady=10)
        # cancle button
        btn_cancle = tk.Button(self.root, text="Cancel", command=self.cancle_button, width = 20)
        btn_cancle.pack(side=tk.RIGHT)




    class Block():
        def __init__(self, block_num, frame, settings, fontStyleRegular, column_id):
            """helper class for drawing a block (compricing of probabilites and length) on tkinter user input window

            Args:
                block_num (int): integer for block number (0-3 for now)
                frame (tkinter frame): frame to draw the block in
                settings (TrialParameterHandler object): the object for all the session parameters from TrialPArameterHandler
                fontStyleRegular (tkinter font):
                column_id (int): column in tkinter frame to draw the block to
            """
            self.num = block_num
            self.settings = settings
            self.text = "Block " + str(self.num+1) +": "

            lbl_blk_name = tk.Label(frame, text=self.text, font=fontStyleRegular)
            lbl_blk_name.grid(row=0, column=column_id, padx=10, pady=(5,0))
            # first frame
            #heading
            frame0 = tk.Frame(frame, bg="gray86")
            frame0.grid(row=1, column=column_id, padx=10, pady=(0,10))
            #trial range
            frame1 = tk.Frame(frame0, bg="gray86")
            frame1.grid(row=0, column=0)
            lbl_trial_range = tk.Label(frame1, text="Trial Range:", font=fontStyleRegular, bg="gray86")
            lbl_trial_range.grid(row=0, column=0, padx=(10,5), pady=5, sticky='E')

            self.var_range_min = tk.StringVar(frame1, value=self.settings.blocks[self.num]["trial_range_block"][0])
            self.etr_range_min = tk.Entry(frame1, textvariable=self.var_range_min, width=4)
            self.etr_range_min.grid(row=0, column=1, padx=(0,2), pady=5, sticky='W')

            lbl_rial_til = tk.Label(frame1, text="to", font=fontStyleRegular, bg="gray86")
            lbl_rial_til.grid(row=0, column=2, pady=5, sticky='W')

            self.var_range_max = tk.StringVar(frame1, value=self.settings.blocks[self.num]["trial_range_block"][1])
            self.etr_range_max = tk.Entry(frame1, textvariable=self.var_range_max, width=4)
            self.etr_range_max.grid(row=0, column=3, padx=(0,10), pady=5, sticky='W')

            # second frame
            # prob gamble
            frame2 = tk.Frame(frame0, bg="gray86")
            frame2.grid(row=1, column=0)

            lbl_prob_gb = tk.Label(frame2, text="Probability gamble [0-100]:", font=fontStyleRegular, bg="gray86")
            lbl_prob_gb.grid(row=0, column=0, padx=(10,5), sticky='E')

            self.var_prob_gb = tk.StringVar(frame2, value=self.settings.blocks[self.num]["prob_reward_gamble_block"])
            self.etr_prob_gb = tk.Entry(frame2, textvariable=self.var_prob_gb, width=6)
            self.etr_prob_gb.grid(row=0, column=2, padx=(0,2), sticky='W')
            # prob save
            lbl_rial_range = tk.Label(frame2, text="Probability save [0-100]:", font=fontStyleRegular, bg="gray86")
            lbl_rial_range.grid(row=1, column=0, padx=(10,5), pady=5, sticky='E')

            self.var_prob_save = tk.StringVar(frame2, value=self.settings.blocks[self.num]["prob_reward_save_block"])
            self.etr_prob_save = tk.Entry(frame2, textvariable=self.var_prob_save, width=6)
            self.etr_prob_save.grid(row=1, column=2, padx=(0,10), pady=5, sticky='W')





    class Time():
        def __init__(self, frame ,row_idx, fontStyleRegular, name, dict_value, descr):
            """helper class to draw time rows in tkinter window

            Args:
                frame (tkinter frame): frame in main window to draw in
                row_idx (int): current row to draw in from frame
                fontStyleRegular (tkinter font): [description]
                name (str): variable name of current row
                dict_value (int): value forom time dict representing the value of time variable for current row
                descr (str): description string of current row
            """
            # name
            lbl_name = tk.Label(frame, text=name, font=fontStyleRegular)
            lbl_name.grid(row=row_idx, column=0, padx=(10,10), pady=5, sticky='E')

            #input
            self.var = tk.StringVar(frame, value=dict_value)
            self.etr = tk.Entry(frame, textvariable=self.var, width=4)
            self.etr.grid(row=row_idx, column=1, sticky='W')

            # description
            lbl_desc = tk.Label(frame, text=descr, font=fontStyleRegular, fg='gray66')
            lbl_desc.grid(row=row_idx, column=2, padx=(10,5), sticky='W')
