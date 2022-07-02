import tkinter as tk
import tkinter.font as font
from tkinter import filedialog, ttk
from typing import List

from maxland.parameter_handler import TrialParameterHandler
from maxland.types_usersettings import GambleSide

WINDOW_SIZE = [855, 1000]
CANVAS_SIZE = [835, 920]
WINDOW_SIZE_GAMBLE_TASK = [855, 920]
WINDOW_SIZE_CONFIDENTIALITY_TASK = [855, 1070]


class UserInput:
    """
    tkinter object to create user input window to update sessions parameter from preread userinputs file
    Args: settings (TrialPArameterHandler object): the object for all the session parameters from TrialPArameterHandler
    """

    def __init__(self, settings: TrialParameterHandler):
        self.settings = settings
        self.task = self.settings.task_name
        # setup tkinter variables
        self.root = tk.Tk()
        self.container = ttk.Frame(self.root)
        self.canvas = tk.Canvas(self.container, width=CANVAS_SIZE[0], height=CANVAS_SIZE[1])
        self.canvas.bind_all("<MouseWheel>", self.update_frame_on_scroll)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.root.title("Maxland")
        self.root.geometry(self.get_geometry())
        self.fontStyleBold = font.Font(family="Calibri", size=20)
        self.fontStyleRegular = font.Font(family="Calibri", size=11)
        self.fontStyleBox = font.Font(family="Calibri", size=10)
        # variables for user input
        self.check_weight = False
        self.padx = 30
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_frame_on_scroll(self, event) -> None:
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def update_settings(self):
        self.settings.life_plot = bool(self.var_liveplot.get())

        self.settings.time_dict["time_start"] = float(self.time_start.var.get())
        self.settings.time_dict["time_wheel_stopping_check"] = float(self.time_wheel_stopping_check.var.get())
        self.settings.time_dict["time_wheel_stopping_punish"] = float(self.time_wheel_stopping_punish.var.get())
        self.settings.time_dict["time_present_stimulus"] = float(self.time_present_stimulus.var.get())
        self.settings.time_dict["time_open_loop"] = float(self.time_open_loop.var.get())
        self.settings.time_dict["time_stimulus_freeze"] = float(self.time_stimulus_freeze.var.get())
        self.settings.time_dict["time_reward"] = float(self.time_reward.var.get())
        self.settings.time_dict["time_no_reward"] = float(self.time_reward.var.get())
        self.settings.time_dict["time_inter_trial"] = float(self.time_inter_trial.var.get())
        self.settings.time_dict["time_open_loop_fail_punish"] = float(self.time_open_loop_fail_punish.var.get())

        self.settings.set_min_time_inter_trial()
        self.settings.rotaryencoder_thresholds[0] = int(self.var_rotary_thresh_left.get())
        self.settings.rotaryencoder_thresholds[1] = int(self.var_rotary_thresh_right.get())
        self.settings.stimulus_end_position = [
            int(self.var_stimulus_end_pos_left.get()),
            int(self.var_stimulus_end_pos_right.get()),
        ]
        try:
            self.settings.animal_weight = float(self.var_animal_weight.get())
        except ValueError:
            pass

        self.settings.life_plot = bool(self.var_liveplot.get())  # plot live or not
        self.settings.background_color = list(map(int, self.var_background_color.get().split(",")))

        self.settings.stimulus_radius = int(self.var_stim_rad.get())
        self.settings.stimulus_color = list(map(int, self.var_stim_col.get().split(",")))

        if self.task == "gamble":
            self.settings.gamble_side = self.var_gamble_side.get()
            self.settings.blocks = self.set_new_probability_blocks()
            self.settings.big_reward = float(self.var_big_reward.get())
            self.settings.small_reward = float(self.var_small_reward.get())
            self.settings.update_parameters()

        if self.task == "conf":
            self.settings.trial_number = int(self.var_trial_num.get())
            self.settings.reward = float(self.var_reward.get())

            self.settings.stimulus_correct_side = {
                "grating_sf": float(self.var_stim_correct_frequency.get()),
                "grating_ori": float(self.var_stim_correct_or.get()),
                "grating_size": float(self.var_stim_correct_size.get()),
                "grating_speed": float(self.var_stim_correct_phase_speed.get()),
            }
            self.settings.stimulus_wrong_side = {
                "grating_sf": float(self.var_stim_wrong_frequency.get()),
                "grating_ori": float(self.var_stim_wrong_or.get()),
                "grating_size": float(self.var_stim_wrong_size.get()),
                "grating_speed": float(self.var_stim_wrong_phase_speed.get()),
            }
            self.settings.stimulus_type = self.var_drp_stim.get()

            self.settings.reward = float(self.var_reward.get())
            self.settings.insist_range_trigger = int(self.var_insist_range_trigger.get())
            self.settings.insist_range_deactivate = int(self.var_insist_range_deact.get())
            self.settings.insist_correct_deactivate = int(self.var_insist_cor.get())
            self.settings.time_dict["time_range_noreward_punish"] = [
                float(self.time_no_reward_punish.var_1.get()),
                float(self.time_no_reward_punish.var_2.get()),
            ]
            self.settings.update_parameters()

    def update_settings_after_session(self):
        self.settings.manual_reward = self.var_reward_manual.get()
        self.settings.animal_weight_after = self.var_animal_weight_after.get()
        self.settings.notes = self.notes.get("1.0", "end")

    def get_geometry(self):
        if self.task == "gamble":
            self.window_size = WINDOW_SIZE_GAMBLE_TASK
        if self.task == "conf":
            self.window_size = WINDOW_SIZE_CONFIDENTIALITY_TASK
        else:
            self.window_size = WINDOW_SIZE

        screen_size = [self.root.winfo_screenwidth(), self.root.winfo_screenheight()]
        window_offset = [int((screen_size[0] - self.window_size[0]) / 2), 0]
        if self.window_size[0] > screen_size[0]:
            self.window_size[0] = screen_size[0]
            window_offset[0] = 0
        if self.window_size[1] > screen_size[1]:
            self.window_size[1] = screen_size[1] - 100
            window_offset[1] = 0
        return str(self.window_size[0]) + "x" + str(self.window_size[1]) + "+" + str(window_offset[0]) + "+" + str(window_offset[1])

    def on_confirm(self):
        self.update_settings()
        self.settings.run_session = True
        self.root.destroy()

    def on_confirm_after_session(self):
        """ok button for window after session"""
        self.update_settings_after_session()
        self.root.destroy()

    def on_close(self):
        self.settings.run_session = False
        self.root.destroy()

    def on_cancel(self):
        self.on_close()

    def show_window(self):
        self.container.pack()
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.root.mainloop()

    def is_float(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def draw_window_before(self, stage: str = None):
        if self.task == "gamble":
            self.draw_window_before_gamble()
        if self.task == "conf":
            self.draw_window_before_conf(stage)

    def draw_window_after(self):
        if self.task == "gamble":
            self.draw_window_after_gamble()
        if self.task == "conf":
            pass

    # Gamble Task Specific Settings =======================================================
    def stimulus_file_dialog_button(self):
        stim_file = filedialog.askopenfilename(
            initialdir="../../stimulus/",
            title="Select file",
            filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")),
        )
        self.settings.stim = stim_file

    def set_new_probability_blocks(self):
        block_list = []
        for block in self.blocks:
            block_dict = {}
            block_dict["trial_range_block"] = [
                int(block.var_range_min.get()),
                int(block.var_range_max.get()),
            ]
            block_dict["prob_reward_gamble_block"] = float(block.var_prob_gb.get())
            block_dict["prob_reward_save_block"] = float(block.var_prob_save.get())
            block_list.append(block_dict)
        return block_list

    def draw_window_before_gamble(self):
        ttk.Label(self.scrollable_frame, text="Gamble Task Settings").pack()
        ttk.Label(self.scrollable_frame, text="ESSENTIAL SETTINGS", foreground="gray66").pack(anchor=tk.W, padx=(10, 2))
        frame_1 = tk.Frame(self.scrollable_frame, highlightbackground="black", highlightthickness=1)
        frame_1.pack(fill=tk.BOTH, padx=self.padx, pady=(2, 10))

        lbl_gamble_side = tk.Label(frame_1, text="Gamble Side:", font=self.fontStyleRegular)
        lbl_gamble_side.grid(row=0, column=0, padx=5, pady=8)
        self.var_gamble_side = tk.StringVar(frame_1)
        self.var_gamble_side.set(self.settings.gamble_side)
        dd_gamble_side = tk.OptionMenu(frame_1, self.var_gamble_side, GambleSide.LEFT, GambleSide.RIGHT)
        dd_gamble_side.grid(row=0, column=1)

        lbl_animal_weight = tk.Label(frame_1, text="Animal weight:", font=self.fontStyleRegular)
        lbl_animal_weight.grid(row=0, column=3, padx=(20, 5), pady=8)
        self.var_animal_weight = tk.StringVar(frame_1)
        self.etr_animal_weight = tk.Entry(frame_1, textvariable=self.var_animal_weight)
        self.etr_animal_weight.grid(row=0, column=4, pady=8)

        self.var_liveplot = tk.IntVar(
            frame_1,
        )
        self.var_liveplot.set(self.settings.life_plot)
        self.btn_liveplot = tk.Checkbutton(frame_1, text="Life Plotting", variable=self.var_liveplot)
        self.btn_liveplot.grid(row=0, column=5, sticky="W", padx=20)

        # frame blocks
        tk.Label(self.scrollable_frame, text="BLOCKS", font=self.fontStyleBox, fg="gray66").pack(
            anchor=tk.W, padx=self.padx - 2, pady=(10, 2)
        )
        frame_2 = tk.Frame(self.scrollable_frame, highlightbackground="black", highlightthickness=1)
        frame_2.pack(fill=tk.BOTH, padx=self.padx, pady=2)

        blk0 = self.Block(0, frame_2, self.settings, self.fontStyleRegular, 0)
        blk1 = self.Block(1, frame_2, self.settings, self.fontStyleRegular, 1)
        blk2 = self.Block(2, frame_2, self.settings, self.fontStyleRegular, 2)

        self.blocks = [blk0, blk1, blk2]

        # frame rewards
        tk.Label(self.scrollable_frame, text="REWARD", font=self.fontStyleBox, fg="gray66").pack(
            anchor=tk.W, padx=self.padx - 2, pady=(15, 2)
        )
        frame_3 = tk.Frame(self.scrollable_frame, highlightbackground="black", highlightthickness=1)
        frame_3.pack(fill=tk.BOTH, padx=self.padx, pady=2)

        lbl_big_reward = tk.Label(frame_3, text="Gamble side reward [ml]:", font=self.fontStyleRegular)
        lbl_big_reward.grid(row=0, column=0, padx=5, pady=8)
        self.var_big_reward = tk.StringVar(frame_3, value=self.settings.big_reward)
        self.etr_big_reward = tk.Entry(frame_3, textvariable=self.var_big_reward, width=10)
        self.etr_big_reward.grid(row=0, column=1, pady=8)

        lbl_small_reward = tk.Label(frame_3, text="Save side reward [ml]:", font=self.fontStyleRegular)
        lbl_small_reward.grid(row=0, column=2, padx=(30, 5), pady=8)
        self.var_small_reward = tk.StringVar(frame_3, value=self.settings.small_reward)
        self.etr_small_reward = tk.Entry(frame_3, textvariable=self.var_small_reward, width=10)
        self.etr_small_reward.grid(row=0, column=3, pady=8)

        calibrate_text = "Last time calibrated: " + self.settings.last_callibration
        lbl_last_calibrate = tk.Label(frame_3, text=calibrate_text, font=self.fontStyleRegular)
        lbl_last_calibrate.grid(row=0, column=4, padx=(30, 5), pady=8)

        # frame stimulus
        tk.Label(self.scrollable_frame, text="STIMULUS", font=self.fontStyleBox, fg="gray66").pack(
            anchor=tk.W, padx=self.padx - 2, pady=(15, 2)
        )
        frame_4 = tk.Frame(self.scrollable_frame, highlightbackground="black", highlightthickness=1)
        frame_4.pack(fill=tk.BOTH, padx=self.padx, pady=2)

        # frame row 0
        frame_4_0 = tk.Frame(frame_4)
        frame_4_0.grid(row=0, column=0, sticky="W")

        # background color
        lbl_background_color = tk.Label(frame_4_0, text="Window Background:", font=self.fontStyleRegular)
        lbl_background_color.grid(row=0, column=0, padx=(10, 5), pady=8)

        self.var_background_color = tk.StringVar(frame_4_0, value=(",".join(map(str, self.settings.background_color))))
        self.etr_background_color = tk.Entry(frame_4_0, textvariable=self.var_background_color, width=9)
        self.etr_background_color.grid(row=0, column=1, padx=(0, 2), pady=8, sticky="W")

        lbl_stim_rad = tk.Label(frame_4_0, text="Stim size radius [pix]:", font=self.fontStyleRegular)
        lbl_stim_rad.grid(row=0, column=2, padx=(10, 2), pady=8)
        self.var_stim_rad = tk.StringVar(frame_4_0, value=self.settings.stimulus_radius)
        self.etr_stim_rad = tk.Entry(frame_4_0, textvariable=self.var_stim_rad, width=4)
        self.etr_stim_rad.grid(row=0, column=3, padx=(0, 2), pady=8, sticky="W")

        lbl_stim_col = tk.Label(frame_4_0, text="Stim color [RGB]:", font=self.fontStyleRegular)
        lbl_stim_col.grid(row=0, column=4, padx=(10, 2), pady=8)
        self.var_stim_col = tk.StringVar(frame_4_0, value=(",".join(map(str, self.settings.stimulus_color))))
        self.etr_stim_col = tk.Entry(frame_4_0, textvariable=self.var_stim_col, width=9)
        self.etr_stim_col.grid(row=0, column=5, padx=(0, 2), pady=8, sticky="W")

        # frame row 1
        frame_4_1 = tk.Frame(frame_4)
        frame_4_1.grid(row=1, column=0)
        # stimulus end position
        lbl_stimulus_position = tk.Label(frame_4_1, text="Stim end pos [px]:", font=self.fontStyleRegular)
        lbl_stimulus_position.grid(row=1, column=0, padx=(10, 5), pady=8)

        self.var_stimulus_end_pos_left = tk.StringVar(frame_4_1, value=self.settings.stimulus_end_position[0])
        self.etr_stimulus_end_pos_left = tk.Entry(frame_4_1, textvariable=self.var_stimulus_end_pos_left, width=6)
        self.etr_stimulus_end_pos_left.grid(row=1, column=1, padx=(0, 2), pady=8, sticky="W")

        lbl_stim_til = tk.Label(frame_4_1, text="to", font=self.fontStyleRegular)
        lbl_stim_til.grid(row=1, column=2, pady=8, sticky="W")

        self.var_stimulus_end_pos_right = tk.StringVar(frame_4_1, value=self.settings.stimulus_end_position[1])
        self.etr_stimulus_end_pos_right = tk.Entry(frame_4_1, textvariable=self.var_stimulus_end_pos_right, width=6)
        self.etr_stimulus_end_pos_right.grid(row=1, column=3, padx=(2, 10), pady=8, sticky="W")

        # # wheel rotation
        lbl_stimulus_position = tk.Label(frame_4_1, text="Wheel threshold [deg]:", font=self.fontStyleRegular)
        lbl_stimulus_position.grid(row=1, column=4, padx=(10, 5), pady=8)

        self.var_rotary_thresh_left = tk.StringVar(frame_4_1, value=self.settings.rotaryencoder_thresholds[0])
        self.etr_rotary_thresh_left = tk.Entry(frame_4_1, textvariable=self.var_rotary_thresh_left, width=8)
        self.etr_rotary_thresh_left.grid(row=1, column=5, padx=(0, 2), pady=8, sticky="W")

        lbl_wheel_til = tk.Label(frame_4_1, text="to", font=self.fontStyleRegular)
        lbl_wheel_til.grid(row=1, column=6, pady=8, sticky="W")

        self.var_rotary_thresh_right = tk.StringVar(frame_4_1, value=self.settings.rotaryencoder_thresholds[1])
        self.etr_rotary_thresh_right = tk.Entry(frame_4_1, textvariable=self.var_rotary_thresh_right, width=8)
        self.etr_rotary_thresh_right.grid(row=1, column=7, padx=(2, 10), pady=8, sticky="W")

        # frame time
        tk.Label(self.scrollable_frame, text="TIME", font=self.fontStyleBox, fg="gray66").pack(
            anchor=tk.W, padx=self.padx - 2, pady=(15, 2)
        )
        frame_5 = tk.Frame(self.scrollable_frame, highlightbackground="black", highlightthickness=1)
        frame_5.pack(fill=tk.BOTH, padx=self.padx, pady=2)

        frame_5_0 = tk.Frame(frame_5)
        frame_5_0.grid(row=0, column=0, pady=8, sticky="W")

        # row 0
        self.time_start = self.Time(
            frame_5_0,
            0,
            self.fontStyleRegular,
            "Start wait",
            self.settings.time_dict["time_start"],
            "time before the trial starts",
        )
        # row 1
        self.time_wheel_stopping_check = self.Time(
            frame_5_0,
            1,
            self.fontStyleRegular,
            "Wheel topping check window",
            self.settings.time_dict["time_wheel_stopping_check"],
            "time window the wheel has to be stopped",
        )
        # row 2
        self.time_wheel_stopping_punish = self.Time(
            frame_5_0,
            2,
            self.fontStyleRegular,
            "Wheel not stopping punish",
            self.settings.time_dict["time_wheel_stopping_punish"],
            "time to wait before new trial starts, if the wheel is not stopped",
        )
        # row 3
        self.time_present_stimulus = self.Time(
            frame_5_0,
            3,
            self.fontStyleRegular,
            "Stimulus presentation",
            self.settings.time_dict["time_present_stimulus"],
            "time stimulus is presented but not movable",
        )
        # row 4
        self.time_open_loop = self.Time(
            frame_5_0,
            4,
            self.fontStyleRegular,
            "Open loop",
            self.settings.time_dict["time_open_loop"],
            "time of open loop where wheel moves the stimulus",
        )
        # row 5
        self.time_open_loop_fail_punish = self.Time(
            frame_5_0,
            5,
            self.fontStyleRegular,
            "Open loop fail punish",
            self.settings.time_dict["time_open_loop_fail_punish"],
            "time wait if stimulus not moved far enough to position",
        )
        # row 6
        self.time_stimulus_freeze = self.Time(
            frame_5_0,
            6,
            self.fontStyleRegular,
            "Stimulus freeze",
            self.settings.time_dict["time_stimulus_freeze"],
            "time stimulus is presented at reached position but not movable anymore",
        )
        # row 7
        self.time_reward = self.Time(
            frame_5_0,
            7,
            self.fontStyleRegular,
            "Reward time",
            self.settings.time_dict["time_reward"],
            "time the animal has for the reward = valve open + time after",
        )
        # row 8
        self.time_inter_trial = self.Time(
            frame_5_0,
            8,
            self.fontStyleRegular,
            "Inter trial",
            self.settings.time_dict["time_inter_trial"],
            "time at end of each Trial",
        )

        btn_ok = tk.Button(self.scrollable_frame, text="OK", command=self.on_confirm, width=20)
        btn_ok.pack(side=tk.RIGHT, padx=self.padx, pady=10)
        btn_cancel = tk.Button(self.scrollable_frame, text="Cancel", command=self.on_cancel, width=20)
        btn_cancel.pack(side=tk.RIGHT)

    def draw_window_after_gamble(self):
        """tkinter window to get user input after session, variables and default values are read from settings object"""
        tk.Label(self.scrollable_frame, text="Gamble Task Report", font=self.fontStyleBold).pack()

        # frame essential input
        tk.Label(self.scrollable_frame, text="ESSENTIAL SETTINGS", font=self.fontStyleBox, fg="gray66").pack(
            anchor=tk.W, padx=self.padx - 2
        )
        frame_1 = tk.Frame(self.scrollable_frame, highlightbackground="black", highlightthickness=1)
        frame_1.pack(fill=tk.BOTH, padx=self.padx, pady=(2, 10))

        # animal weight input
        lbl_animal_weight = tk.Label(frame_1, text="Animal weight after:", font=self.fontStyleRegular)
        lbl_animal_weight.grid(row=0, column=3, padx=(20, 5), pady=8)
        self.var_animal_weight_after = tk.StringVar(frame_1)
        self.etr_animal_weight_after = tk.Entry(frame_1, textvariable=self.var_animal_weight_after)
        self.etr_animal_weight_after.grid(row=0, column=4, pady=8)

        # frame manual rewards
        tk.Label(self.scrollable_frame, text="MANUAL REWARD", font=self.fontStyleBox, fg="gray66").pack(
            anchor=tk.W, padx=self.padx - 2, pady=(15, 2)
        )
        frame_3 = tk.Frame(self.scrollable_frame, highlightbackground="black", highlightthickness=1)
        frame_3.pack(fill=tk.BOTH, padx=self.padx, pady=2)
        lbl_reward = tk.Label(frame_3, text="Manual administered reward [ml]:", font=self.fontStyleRegular)
        lbl_reward.grid(row=0, column=0, padx=5, pady=8)

        self.var_reward_manual = tk.StringVar(frame_1)
        self.etr_reward_manual = tk.Entry(frame_3, textvariable=self.var_reward_manual, width=10)
        self.etr_reward_manual.grid(row=0, column=1, pady=8)

        # frame time
        tk.Label(self.scrollable_frame, text="NOTES", font=self.fontStyleBox, fg="gray66").pack(
            anchor=tk.W, padx=self.padx - 2, pady=(15, 2)
        )

        scrollbar = tk.Scrollbar(self.scrollable_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.notes = tk.Text(
            self.scrollable_frame,
            highlightbackground="black",
            highlightthickness=1,
            height=38,
            width=10,
        )
        self.notes.pack(fill=tk.BOTH, padx=self.padx, pady=2)

        scrollbar.config(command=self.notes.yview)
        self.notes.config(yscrollcommand=scrollbar.set)

        btn_ok = tk.Button(self.scrollable_frame, text="OK", command=self.on_confirm_after_session, width=20)
        btn_ok.pack(side=tk.RIGHT, padx=self.padx, pady=10)
        btn_cancel = tk.Button(self.scrollable_frame, text="Cancel", command=self.on_cancel, width=20)
        btn_cancel.pack(side=tk.RIGHT)

    # Confidentiality Task Specific Settings ===============================================
    def draw_window_before_conf(self, stage="training"):
        tk.Label(self.scrollable_frame, text="Confidentiality Task Settings", font=self.fontStyleBold).pack()

        # frame essential input
        tk.Label(self.scrollable_frame, text="ESSENTIAL SETTINGS", font=self.fontStyleBox, fg="gray66").pack(
            anchor=tk.W, padx=self.padx - 2
        )
        frame_1 = tk.Frame(self.scrollable_frame, highlightbackground="black", highlightthickness=1)
        frame_1.pack(fill=tk.BOTH, padx=self.padx, pady=(2, 10))

        # animal weight input
        lbl_animal_weight = tk.Label(frame_1, text="Animal weight:", font=self.fontStyleRegular)
        lbl_animal_weight.grid(row=0, column=3, padx=(20, 5), pady=8)
        self.var_animal_weight = tk.StringVar(frame_1)
        self.etr_animal_weight = tk.Entry(frame_1, textvariable=self.var_animal_weight)
        self.etr_animal_weight.grid(row=0, column=4, pady=8)

        # live plotting
        self.var_liveplot = tk.IntVar(
            frame_1,
        )
        self.var_liveplot.set(self.settings.life_plot)
        self.btn_liveplot = tk.Checkbutton(frame_1, text="Life Plotting", variable=self.var_liveplot)
        self.btn_liveplot.grid(row=0, column=5, sticky="W", padx=20)

        # frame trials
        tk.Label(self.scrollable_frame, text="TRIAL", font=self.fontStyleBox, fg="gray66").pack(
            anchor=tk.W, padx=self.padx - 2, pady=(10, 2)
        )
        frame_2 = tk.Frame(self.scrollable_frame, highlightbackground="black", highlightthickness=1)
        frame_2.pack(fill=tk.BOTH, padx=self.padx, pady=2)

        # trial
        lbl_rials_num = tk.Label(frame_2, text="trial number:", font=self.fontStyleRegular)
        lbl_rials_num.grid(row=0, column=0, padx=5, pady=8)

        self.var_trial_num = tk.StringVar(frame_2, value=self.settings.trial_number)
        self.etr_trial_num = tk.Entry(frame_2, textvariable=self.var_trial_num, width=10)
        self.etr_trial_num.grid(row=0, column=1, pady=8)

        tk.Label(self.scrollable_frame, text="REWARD", font=self.fontStyleBox, fg="gray66").pack(
            anchor=tk.W, padx=self.padx - 2, pady=(10, 2)
        )
        frame_3 = tk.Frame(self.scrollable_frame, highlightbackground="black", highlightthickness=1)
        frame_3.pack(fill=tk.BOTH, padx=self.padx, pady=2)

        # reward
        lbl_reward = tk.Label(frame_3, text="reward [ml]:", font=self.fontStyleRegular)
        lbl_reward.grid(row=0, column=2, padx=5, pady=8)

        self.var_reward = tk.StringVar(frame_3, value=self.settings.reward)
        self.etr_reward = tk.Entry(frame_3, textvariable=self.var_reward, width=10)
        self.etr_reward.grid(row=0, column=3, pady=8)

        # last time calibrated
        calibrate_text = "Last time calibrated: " + self.settings.last_callibration
        lbl_last_calibrate = tk.Label(frame_3, text=calibrate_text, font=self.fontStyleRegular)
        lbl_last_calibrate.grid(row=0, column=4, padx=(30, 5), pady=8)

        # frame stimulus
        tk.Label(self.scrollable_frame, text="STIMULUS", font=self.fontStyleBox, fg="gray66").pack(
            anchor=tk.W, padx=self.padx - 2, pady=(15, 2)
        )
        frame_4 = tk.Frame(self.scrollable_frame, highlightbackground="black", highlightthickness=1)
        frame_4.pack(fill=tk.BOTH, padx=self.padx, pady=2)

        # frame row 1
        frame_4_1 = tk.Frame(frame_4)
        frame_4_1.grid(row=1, column=0)

        lbl_background_color = tk.Label(frame_4_1, text="Window Background:", font=self.fontStyleRegular)
        lbl_background_color.grid(row=0, column=0, padx=(10, 5), pady=8)
        self.var_background_color = tk.StringVar(frame_4_1, value=(",".join(map(str, self.settings.background_color))))
        self.etr_background_color = tk.Entry(frame_4_1, textvariable=self.var_background_color, width=9)
        self.etr_background_color.grid(row=0, column=1, padx=(0, 2), pady=8, sticky="W")

        lbl_stimulus_position = tk.Label(frame_4_1, text="Stim end pos [px]:", font=self.fontStyleRegular)
        lbl_stimulus_position.grid(row=0, column=2, padx=(10, 2), pady=8)
        self.var_stimulus_end_pos_left = tk.StringVar(frame_4_1, value=self.settings.stimulus_end_position[0])
        self.etr_stimulus_end_pos_left = tk.Entry(frame_4_1, textvariable=self.var_stimulus_end_pos_left, width=4)
        self.etr_stimulus_end_pos_left.grid(row=0, column=3, padx=(0, 2), pady=8, sticky="W")
        lbl_stim_til = tk.Label(frame_4_1, text="to", font=self.fontStyleRegular)
        lbl_stim_til.grid(row=0, column=4, pady=8, sticky="W")
        self.var_stimulus_end_pos_right = tk.StringVar(frame_4_1, value=self.settings.stimulus_end_position[1])
        self.etr_stimulus_end_pos_right = tk.Entry(frame_4_1, textvariable=self.var_stimulus_end_pos_right, width=4)
        self.etr_stimulus_end_pos_right.grid(row=0, column=5, padx=(2, 10), pady=8, sticky="W")

        # # wheel rotation
        lbl_stimulus_position = tk.Label(frame_4_1, text="Wheel threhsold [deg]:", font=self.fontStyleRegular)
        lbl_stimulus_position.grid(row=0, column=6, padx=(10, 5), pady=8)

        self.var_rotary_thresh_left = tk.StringVar(frame_4_1, value=self.settings.rotaryencoder_thresholds[0])
        self.etr_rotary_thresh_left = tk.Entry(frame_4_1, textvariable=self.var_rotary_thresh_left, width=4)
        self.etr_rotary_thresh_left.grid(row=0, column=7, padx=(0, 2), pady=8, sticky="W")

        lbl_wheel_til = tk.Label(frame_4_1, text="to", font=self.fontStyleRegular)
        lbl_wheel_til.grid(row=0, column=8, pady=8, sticky="W")

        self.var_rotary_thresh_right = tk.StringVar(frame_4_1, value=self.settings.rotaryencoder_thresholds[1])
        self.etr_rotary_thresh_right = tk.Entry(frame_4_1, textvariable=self.var_rotary_thresh_right, width=4)
        self.etr_rotary_thresh_right.grid(row=0, column=9, padx=(2, 10), pady=8, sticky="W")

        # frame stimulus detail =====================================================================
        frame_5 = tk.Frame(self.scrollable_frame)
        frame_5.pack(fill=tk.BOTH, padx=self.padx, pady=0)

        # frame_5_0 correct ================
        frame_5_0 = tk.Frame(frame_5, highlightbackground="black", highlightthickness=1)
        frame_5_0.grid(row=0, column=0, padx=[0, 2])
        lbl_stim_correct = tk.Label(frame_5_0, text="CORRECT", font=self.fontStyleRegular)
        lbl_stim_correct.grid(row=0, column=0, pady=[8, 0], columnspan=4)
        # frequency
        lbl_stim_correct_frequency = tk.Label(frame_5_0, text="Spatial Frequency:", font=self.fontStyleRegular)
        lbl_stim_correct_frequency.grid(row=1, column=0, padx=(10, 0), pady=0, sticky="E")

        self.var_stim_correct_frequency = tk.StringVar(frame_5_0, value=self.settings.stimulus_correct_side["grating_sf"])
        self.etr_stim_correct_frequency = tk.Entry(frame_5_0, textvariable=self.var_stim_correct_frequency, width=4)
        self.etr_stim_correct_frequency.grid(row=1, column=1, padx=(0, 0), pady=0, sticky="W")
        # orientation
        lbl_stim_correct_or = tk.Label(frame_5_0, text="Orientation:", font=self.fontStyleRegular)
        lbl_stim_correct_or.grid(row=1, column=2, padx=(10, 2), pady=0, sticky="E")

        self.var_stim_correct_or = tk.StringVar(frame_5_0, value=self.settings.stimulus_correct_side["grating_ori"])
        self.etr_stim_correct_or = tk.Entry(frame_5_0, textvariable=self.var_stim_correct_or, width=4)
        self.etr_stim_correct_or.grid(row=1, column=3, padx=(0, 10), pady=10, sticky="W")

        # size
        lbl_stim_correct_size = tk.Label(frame_5_0, text="Size [deg]:", font=self.fontStyleRegular)
        lbl_stim_correct_size.grid(row=2, column=0, padx=(10, 2), pady=0, sticky="E")

        self.var_stim_correct_size = tk.StringVar(frame_5_0, value=self.settings.stimulus_correct_side["grating_size"])
        self.etr_stim_correct_size = tk.Entry(frame_5_0, textvariable=self.var_stim_correct_size, width=4)
        self.etr_stim_correct_size.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="W")

        # speed change
        lbl_stim_correct_speed = tk.Label(frame_5_0, text="Phase Speed:", font=self.fontStyleRegular)
        lbl_stim_correct_speed.grid(row=2, column=2, padx=(10, 2), pady=0, sticky="E")

        self.var_stim_correct_phase_speed = tk.StringVar(frame_5_0, value=self.settings.stimulus_correct_side["grating_speed"])
        self.etr_stim_correct_speed = tk.Entry(frame_5_0, textvariable=self.var_stim_correct_phase_speed, width=4)
        self.etr_stim_correct_speed.grid(row=2, column=3, padx=(0, 10), pady=10, sticky="W")

        # frame_5_1 wrong ================
        frame_5_1 = tk.Frame(frame_5, highlightbackground="black", highlightthickness=1)
        frame_5_1.grid(row=0, column=1, padx=[2, 0])
        lbl_stim_wrong = tk.Label(frame_5_1, text="WRONG", font=self.fontStyleRegular)
        lbl_stim_wrong.grid(row=0, column=0, pady=[8, 0], columnspan=4)
        # frequency
        lbl_stim_wrong_frequency = tk.Label(frame_5_1, text="Spatial Frequency:", font=self.fontStyleRegular)
        lbl_stim_wrong_frequency.grid(row=1, column=0, padx=(10, 0), pady=0, sticky="E")

        self.var_stim_wrong_frequency = tk.StringVar(frame_5_1, value=self.settings.stimulus_wrong_side["grating_sf"])
        self.etr_stim_wrong_frequency = tk.Entry(frame_5_1, textvariable=self.var_stim_wrong_frequency, width=4)
        self.etr_stim_wrong_frequency.grid(row=1, column=1, padx=(0, 0), pady=0, sticky="W")
        # orientation
        lbl_stim_wrong_or = tk.Label(frame_5_1, text="Orientation:", font=self.fontStyleRegular)
        lbl_stim_wrong_or.grid(row=1, column=2, padx=(10, 2), pady=0, sticky="E")

        self.var_stim_wrong_or = tk.StringVar(frame_5_1, value=self.settings.stimulus_wrong_side["grating_ori"])
        self.etr_stim_wrong_or = tk.Entry(frame_5_1, textvariable=self.var_stim_wrong_or, width=4)
        self.etr_stim_wrong_or.grid(row=1, column=3, padx=(0, 10), pady=10, sticky="W")

        # size
        lbl_stim_wrong_size = tk.Label(frame_5_1, text="Size [deg]:", font=self.fontStyleRegular)
        lbl_stim_wrong_size.grid(row=2, column=0, padx=(10, 2), pady=0, sticky="E")

        self.var_stim_wrong_size = tk.StringVar(frame_5_1, value=self.settings.stimulus_wrong_side["grating_size"])
        self.etr_stim_wrong_size = tk.Entry(frame_5_1, textvariable=self.var_stim_wrong_size, width=4)
        self.etr_stim_wrong_size.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="W")

        # speed change
        lbl_stim_wrong_speed = tk.Label(frame_5_1, text="Phase Speed:", font=self.fontStyleRegular)
        lbl_stim_wrong_speed.grid(row=2, column=2, padx=(10, 2), pady=0, sticky="E")

        self.var_stim_wrong_phase_speed = tk.StringVar(frame_5_1, value=self.settings.stimulus_wrong_side["grating_speed"])
        self.etr_stim_wrong_speed = tk.Entry(frame_5_1, textvariable=self.var_stim_wrong_phase_speed, width=4)
        self.etr_stim_wrong_speed.grid(row=2, column=3, padx=(0, 10), pady=10, sticky="W")

        # variable stimulus variables
        frame_6 = tk.Frame(self.scrollable_frame, highlightbackground="black", highlightthickness=1)
        frame_6.pack(fill=tk.BOTH, padx=self.padx, pady=2)

        # select stim type dropdown
        self.var_drp_stim = tk.StringVar()
        self.drp_stim = ttk.Combobox(frame_6, width=12, textvariable=self.var_drp_stim)

        # Adding combobox drop down list
        lbl_drp_stim = tk.Label(frame_6, text="Stimulus Type:", font=self.fontStyleRegular)
        lbl_drp_stim.grid(row=0, column=0, padx=(10, 2), pady=8)

        if stage == "training":
            self.drp_stim["values"] = self.settings.gui_dropdown_list  # ('three-stimuli','two-stimuli','one-stimulus')
            self.drp_stim.grid(column=1, row=0)
            idx = self.settings.gui_dropdown_list.index(self.settings.stimulus_type)
            self.drp_stim.current(idx)  # set current value
        if stage == "habituation_simple":
            list_drp = "three-stimuli"
            self.drp_stim["values"] = list_drp
            self.drp_stim.grid(column=1, row=0)
            idx = self.settings.gui_dropdown_list.index(list_drp)
            self.drp_stim.current(idx)  # set current valu
        if stage == "habituation_complex":
            list_drp = ("three-stimuli", "two-stimuli")
            self.drp_stim["values"] = list_drp
            self.drp_stim.grid(column=1, row=0)
            idx = list_drp.index(self.settings.stimulus_type)
            self.drp_stim.current(idx)  # set current value

        # stimulus radius
        lbl_stim_rad = tk.Label(frame_6, text="Stim size [deg]:", font=self.fontStyleRegular)
        lbl_stim_rad.grid(row=0, column=3, padx=(10, 2), pady=8)

        self.var_stim_rad = tk.StringVar(frame_6, value=self.settings.stimulus_radius)
        self.etr_stim_rad = tk.Entry(frame_6, textvariable=self.var_stim_rad, width=4)
        self.etr_stim_rad.grid(row=0, column=4, padx=(0, 2), pady=8, sticky="W")

        # stimulus color
        lbl_stim_col = tk.Label(frame_6, text="Stim color [RGB]:", font=self.fontStyleRegular)
        lbl_stim_col.grid(row=0, column=5, padx=(10, 2), pady=8)

        self.var_stim_col = tk.StringVar(frame_6, value=(",".join(map(str, self.settings.stimulus_color))))
        self.etr_stim_col = tk.Entry(frame_6, textvariable=self.var_stim_col, width=9)
        self.etr_stim_col.grid(row=0, column=6, padx=(0, 2), pady=8, sticky="W")

        # frame insist mode
        tk.Label(self.scrollable_frame, text="INSIST MODE", font=self.fontStyleBox, fg="gray66").pack(
            anchor=tk.W, padx=self.padx - 2, pady=(15, 2)
        )
        frame_7 = tk.Frame(self.scrollable_frame, highlightbackground="black", highlightthickness=1)
        frame_7.pack(fill=tk.BOTH, padx=self.padx, pady=2)

        lbl_insist_range_trigger = tk.Label(frame_7, text="Insist Mode Trigger Range:", font=self.fontStyleRegular)
        lbl_insist_range_trigger.grid(row=0, column=0, padx=(10, 2), pady=8, sticky="E")
        self.var_insist_range_trigger = tk.StringVar(frame_7, value=self.settings.insist_range_trigger)
        self.etr_insist_range_trigger = tk.Entry(frame_7, textvariable=self.var_insist_range_trigger, width=4)
        self.etr_insist_range_trigger.grid(row=0, column=1, padx=(0, 30), pady=8, sticky="E")

        lbl_insist_cor = tk.Label(
            frame_7,
            text="Correct Number Insist Mode Deactivate:",
            font=self.fontStyleRegular,
        )
        lbl_insist_cor.grid(row=0, column=3, padx=(10, 2), pady=8, sticky="E")

        self.var_insist_cor = tk.StringVar(frame_7, value=self.settings.insist_correct_deactivate)
        self.etr_insist_cor = tk.Entry(frame_7, textvariable=self.var_insist_cor, width=4)
        self.etr_insist_cor.grid(row=0, column=4, padx=(0, 10), pady=8, sticky="E")

        lbl_insist_range_deact = tk.Label(frame_7, text="Insist Mode Deactivate Range:", font=self.fontStyleRegular)
        lbl_insist_range_deact.grid(row=0, column=5, padx=(10, 2), pady=8, sticky="E")
        self.var_insist_range_deact = tk.StringVar(frame_7, value=self.settings.insist_range_deactivate)
        self.etr_insist_range_deact = tk.Entry(frame_7, textvariable=self.var_insist_range_deact, width=4)
        self.etr_insist_range_deact.grid(row=0, column=6, padx=(0, 0), pady=8, sticky="E")

        # frame time
        tk.Label(self.scrollable_frame, text="TIME [seconds]", font=self.fontStyleBox, fg="gray66").pack(
            anchor=tk.W, padx=self.padx - 2, pady=(15, 2)
        )
        frame_7 = tk.Frame(self.scrollable_frame, highlightbackground="black", highlightthickness=1)
        frame_7.pack(fill=tk.BOTH, padx=self.padx, pady=2)

        frame_7_0 = tk.Frame(frame_7)
        frame_7_0.grid(row=0, column=0, pady=8, sticky="W")

        # row 0
        self.time_start = self.Time(
            frame_7_0,
            0,
            self.fontStyleRegular,
            "Start wait Time",
            self.settings.time_dict["time_start"],
            "time bevor the trial starts",
        )
        # row 1
        self.time_wheel_stopping_check = self.Time(
            frame_7_0,
            1,
            self.fontStyleRegular,
            "Stopping check",
            self.settings.time_dict["time_wheel_stopping_check"],
            "time the wheel has to be stopped",
        )
        # row 2
        self.time_wheel_stopping_punish = self.Time(
            frame_7_0,
            2,
            self.fontStyleRegular,
            "WNS punish",
            self.settings.time_dict["time_wheel_stopping_punish"],
            "time wait if the wheel is not stopped before new trial starts",
        )
        # row 3
        self.time_present_stimulus = self.Time(
            frame_7_0,
            3,
            self.fontStyleRegular,
            "Stim Presentation",
            self.settings.time_dict["time_present_stimulus"],
            "time stimulus is presented but not movable",
        )
        # row 4
        self.time_open_loop = self.Time(
            frame_7_0,
            4,
            self.fontStyleRegular,
            "Open Loop",
            self.settings.time_dict["time_open_loop"],
            "time of open loop where wheel moves the stimulus",
        )
        # row 5
        # open loop punish range
        self.time_open_loop_fail_punish = self.Time(
            frame_7_0,
            5,
            self.fontStyleRegular,
            "Open Loop Fail",
            self.settings.time_dict["time_open_loop_fail_punish"],
            "time wait if stimulus not moved far enough to position",
        )
        # row 6
        self.time_stimulus_freeze = self.Time(
            frame_7_0,
            6,
            self.fontStyleRegular,
            "Stim Freez",
            self.settings.time_dict["time_stimulus_freeze"],
            "time stimulus is presented at reached position but not movable anymore",
        )
        # row 7
        self.time_reward = self.Time(
            frame_7_0,
            7,
            self.fontStyleRegular,
            "Reward Time",
            self.settings.time_dict["time_reward"],
            "time the animal has for the reward = valve open + time after",
        )
        # row 8
        self.time_no_reward_punish = self.TimeRange(
            frame_7_0,
            8,
            self.fontStyleRegular,
            "No Reward Punish Time",
            self.settings.time_dict["time_range_no_reward_punish"],
            "time the animal has for the reward = valve open + time after",
        )
        # row 9
        self.time_inter_trial = self.Time(
            frame_7_0,
            9,
            self.fontStyleRegular,
            "Trial End",
            self.settings.time_dict["time_inter_trial"],
            "time at end of each Trial",
        )

        # ok button
        btn_ok = tk.Button(self.scrollable_frame, text="OK", command=self.on_confirm, width=20)
        btn_ok.pack(side=tk.RIGHT, padx=self.padx, pady=10)
        # cancle button
        btn_cancel = tk.Button(self.scrollable_frame, text="Cancel", command=self.on_cancel, width=20)
        btn_cancel.pack(side=tk.RIGHT)

    class Block:
        """
        helper class for drawing a block (compricing of probabilites and length) on tkinter user input window
        Args:
            block_num (int): integer for block number (0-3 for now)
            frame (tkinter frame): frame to draw the block in
            settings (TrialParameterHandler object): the object for all the session parameters from TrialPArameterHandler
            fontStyleRegular (tkinter font):
            column_id (int): column in tkinter frame to draw the block to
        """

        def __init__(
            self,
            block_index: int,
            frame: tk.Frame,
            settings: TrialParameterHandler,
            fontStyleRegular: font.Font,
            column_id: int,
        ):

            self.num = block_index
            self.settings = settings
            self.text = "Block " + str(self.num + 1) + ": "

            lbl_blk_name = tk.Label(frame, text=self.text, font=fontStyleRegular)
            lbl_blk_name.grid(row=0, column=column_id, padx=10, pady=(5, 0))
            # first frame
            # heading
            frame0 = tk.Frame(frame, bg="gray86")
            frame0.grid(row=1, column=column_id, padx=10, pady=(0, 10))
            # trial range
            frame_1 = tk.Frame(frame0, bg="gray86")
            frame_1.grid(row=0, column=0)
            lbl_trial_range = tk.Label(frame_1, text="Trial Range:", font=fontStyleRegular, bg="gray86")
            lbl_trial_range.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="E")

            self.var_range_min = tk.StringVar(frame_1, value=str(self.settings.blocks[self.num]["trial_range_block"][0]))
            self.etr_range_min = tk.Entry(frame_1, textvariable=self.var_range_min, width=4)
            self.etr_range_min.grid(row=0, column=1, padx=(0, 2), pady=5, sticky="W")

            lbl_rial_til = tk.Label(frame_1, text="to", font=fontStyleRegular, bg="gray86")
            lbl_rial_til.grid(row=0, column=2, pady=5, sticky="W")

            self.var_range_max = tk.StringVar(frame_1, value=str(self.settings.blocks[self.num]["trial_range_block"][1]))
            self.etr_range_max = tk.Entry(frame_1, textvariable=self.var_range_max, width=4)
            self.etr_range_max.grid(row=0, column=3, padx=(0, 10), pady=5, sticky="W")

            # second frame
            # prob gamble
            frame_2 = tk.Frame(frame0, bg="gray86")
            frame_2.grid(row=1, column=0)

            lbl_prob_gb = tk.Label(
                frame_2,
                text="Probability gamble [0-100]:",
                font=fontStyleRegular,
                bg="gray86",
            )
            lbl_prob_gb.grid(row=0, column=0, padx=(10, 5), sticky="E")

            self.var_prob_gb = tk.StringVar(frame_2, value=str(self.settings.blocks[self.num]["prob_reward_gamble_block"]))
            self.etr_prob_gb = tk.Entry(frame_2, textvariable=self.var_prob_gb, width=6)
            self.etr_prob_gb.grid(row=0, column=2, padx=(0, 2), sticky="W")
            # prob save
            lbl_rial_range = tk.Label(
                frame_2,
                text="Probability save [0-100]:",
                font=fontStyleRegular,
                bg="gray86",
            )
            lbl_rial_range.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="E")

            self.var_prob_save = tk.StringVar(frame_2, value=str(self.settings.blocks[self.num]["prob_reward_save_block"]))
            self.etr_prob_save = tk.Entry(frame_2, textvariable=self.var_prob_save, width=6)
            self.etr_prob_save.grid(row=1, column=2, padx=(0, 10), pady=5, sticky="W")

    class Time:
        """
        helper class to draw time rows in tkinter window
        Args:
            frame (tkinter frame): frame in main window to draw in
            row_idx (int): current row to draw in from frame
            fontStyleRegular (tkinter font): [description]
            name (str): variable name of current row
            dict_value (int): value from time dict representing the value of time variable for current row
            description (str): description string of current row
        """

        def __init__(
            self,
            frame: tk.Frame,
            row_index: int,
            fontStyleRegular: font.Font,
            name: str,
            time_dict_value: int,
            description: str,
        ):

            # name
            lbl_name = tk.Label(frame, text=name, font=fontStyleRegular)
            lbl_name.grid(row=row_index, column=0, padx=(10, 10), pady=5, sticky="E")

            # input
            self.var = tk.StringVar(frame, value=str(time_dict_value))
            self.etr = tk.Entry(frame, textvariable=self.var, width=4)
            self.etr.grid(row=row_index, column=1, sticky="W")

            # description
            lbl_desc = tk.Label(frame, text=description, font=fontStyleRegular, fg="gray66")
            lbl_desc.grid(row=row_index, column=2, padx=(10, 5), sticky="W", columnspan=5)

    class TimeRange:
        """
        helper class to draw time rows for time range with two entries in tkinter window
        Args:
            frame (tkinter frame): frame in main window to draw in
            row_idx (int): current row to draw in from frame
            fontStyleRegular (tkinter font): [description]
            name (str): variable name of current row
            dict_value (int): [min, max] value from time dict representing the value of time variable for current row
            description (str): description string of current row
        """

        def __init__(
            self,
            frame: tk.Frame,
            row_index: int,
            fontStyleRegular: font.Font,
            name: str,
            time_dict_range: List[int],
            description: str,
        ):

            lbl_name = tk.Label(frame, text=name, font=fontStyleRegular)
            lbl_name.grid(row=row_index, column=0, padx=(10, 10), pady=5, sticky="E")

            # input 1
            self.var_1 = tk.StringVar(frame, value=str(time_dict_range[0]))
            self.etr_1 = tk.Entry(frame, textvariable=self.var_1, width=4)
            self.etr_1.grid(row=row_index, column=1, sticky="W")
            # new frame with 4 columns

            # min label
            lbl_min = tk.Label(frame, text="min", font=fontStyleRegular)
            lbl_min.grid(row=row_index, column=2, padx=(0, 10), pady=5, sticky="W")
            # input 2
            self.var_2 = tk.StringVar(frame, value=str(time_dict_range[1]))
            self.etr_2 = tk.Entry(frame, textvariable=self.var_2, width=4)
            self.etr_2.grid(row=row_index, column=4, sticky="W")
            # min label
            lbl_max = tk.Label(frame, text="max", font=fontStyleRegular)
            lbl_max.grid(row=row_index, column=5, padx=(0, 0), pady=5, sticky="W")

            # description
            lbl_desc = tk.Label(frame, text=description, font=fontStyleRegular, fg="gray66")
            lbl_desc.grid(row=row_index, column=6, padx=(10, 5), sticky="W")
