import time
import tkinter as tk
from tkinter import ttk
#colorhunt.co for color palettes
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
SKY_BLUE = "#87CEEB"
FONT_NAME = "Courier"
NUMBER_OF_SESSIONS_BEFORE_LONG_BREAK = 4
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

def convert_seconds_to_minutes(seconds):
    minutes, seconds = divmod(seconds, 60)
    return minutes, seconds

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.pomodoro_status = "work"
        self.work_counter = 0
        self.timer_running = False
        self.stop_signal_on = False
        self.highest_timer_running = 0 #actually starts at 1, incrementation before implementation
        self.number_of_consecutive_reset_clicks = 0
        self.previous_pomodoro_status = ""


        self.attributes('-topmost',True)
        self.title("Pomodoro Timer")
        self.minsize(width=200, height=220)
        self.config(padx=10, pady=10, bg=YELLOW)
        ttk.Style(self).theme_use('classic') #no effect on mac
        self.set_window_geometry()

        self.create_widgets()
    def set_window_geometry(self):
        w = 200  # width for the Tk root
        h = 220  # height for the Tk root

        # get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws * 9 / 10) - (w / 2)
        y = (hs * 12 / 16) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
    def create_widgets(self):
        #TODO preference add hide button to only have start reset and background changing colour
        self.button_start = tk.Button(text="Start Timer", command=self.pomodoro_button_pressed, highlightbackground=YELLOW)
        # self.button_start.pack(side="left")
        self.button_start.grid(column=0, row=1, pady= (0,10))

        self.button_reset = tk.Button(text="Reset", command=self.reset, highlightbackground=YELLOW)
        # self.button_reset.pack(side="left", padx=30)
        self.button_reset.grid(column=1,row=1, pady= (0,10))

        self.canvas = tk.Canvas(width=180, height=79, bg=YELLOW, highlightthickness=0)
        self.image = tk.PhotoImage(file="tomato.png")
        self.canvas.create_image(90,39, image=self.image) #position relative to canvas
        # self.canvas.create_text(120,86, text="25:00", font=("Arial", 40, "bold"), fill="black")

        # self.canvas.pack(side="top")
        self.canvas.grid(column=0, columnspan=2, row=2)
        # Text Label
        minutes, seconds = convert_seconds_to_minutes(WORK_MIN * 60)
        self.label = tk.Label(text=f"{minutes:>02}:{seconds:<02}", font=("Arial", 40, "bold"), bg=YELLOW, fg= "black")
        # changing options - at init/as_dict/using.config fxn
        # my_label.config(text="New Label Text")
        # my_label.config(padx=25,pady=25)
        # self.label.pack(side="top", expand=False) #PACKER - display management
        # my_label.place(x=70,y=80)
        self.label.grid(column=0, columnspan=2, row=3)  # SNAPS TO TOP LEFT IF EMPTY ROW OR COLUMN IN BETWEEN

        self.label_checkmarks = tk.Label(text= "✓", font=("Arial", 24, "bold"), bg=YELLOW, fg=GREEN)
        # self.label_checkmarks.pack(side="top")
        self.label_checkmarks.grid(column=0, columnspan=2,row=4)


    def countdown_recursive(self, timer_length, id_number, original_timer_length):
        #for future reference - can assign recursive function to name and use tk.window.after_cancel to cancel
        self.timer_running = True
        if timer_length < 0:
            self.timer_running = False
            return
        if self.stop_signal_on:
            self.stop_signal_on = False
            self.timer_running = False
            return

        if id_number < self.highest_timer_running or self.highest_timer_running == 0 :
            self.timer_running = False
            return

        minutes, seconds = convert_seconds_to_minutes(timer_length)
        self.label["text"] = f"{minutes:>02}:{seconds:<02}"
        self.after(1000, self.countdown_recursive, timer_length - 1, id_number, original_timer_length)


    def pomodoro_button_pressed(self):
        #the levels of this function are mismatched - update checkmarks
        # #consecutivereset should be in different place than work timer and work effects
        self.update_checkmarks()
        self.number_of_consecutive_reset_clicks = 0

        self.stop_signal_on = False

        self.highest_timer_running += 1

        # if self.timer_running:
            # NEED TO COLLECT STATUS OF TIMER RUNNING BEFORE TIMER STARTS AND CHANGE
            # STATUS TO BE USED IN COUNTDOWN FUNCTION AFTER NEW TIMER HAS STARTED
            # NEW COUNTDOWN FUNCTION TRIGGERS INSTANTLY THEN OLD
            # WANT NEW TO PASS OK AND OLD TO BE STOPPED
            # ALTERNATIVELY CAN ASSOCIATE ID NUMBER TO RECURSIVE TIMER - AND CHECK IF TIMER ASSOCIATED WITH HIGHEST
            # ID NUMBER ---- IMPLEMENTATION ADDED SUCCESSFULLY - LEGACY CODE KEPT FOR CELEBRATION
            # old_timer_should_stop = True
        self.pomodoro_timer(self.pomodoro_status)
        self.apply_extra_effects(self.pomodoro_status)
        self.pomodoro_status = self.cycle_pomdoro_status(self.pomodoro_status, self.work_counter % NUMBER_OF_SESSIONS_BEFORE_LONG_BREAK == 0)
    def pomodoro_timer(self, timer_type):
        if timer_type == "work":
            self.countdown_recursive(WORK_MIN * 60, self.highest_timer_running, WORK_MIN * 60)
        elif timer_type == "break":
            self.countdown_recursive(SHORT_BREAK_MIN * 60, self.highest_timer_running, SHORT_BREAK_MIN * 60)
        elif timer_type == "long_break":
            self.countdown_recursive(LONG_BREAK_MIN * 60, self.highest_timer_running, LONG_BREAK_MIN * 60)
        else:
            raise NameError("Timer type (status) not set correctly.")


    def update_checkmarks(self):
        self.label_checkmarks["text"] = ""
        for i in range(self.work_counter):
            i = i + 1
            self.label_checkmarks["text"] += "✓"
            if i % NUMBER_OF_SESSIONS_BEFORE_LONG_BREAK == 0:
                self.label_checkmarks["text"] += "\n"

    def apply_extra_effects(self, current_status):
        # TODO preference change bg with change in status
        if current_status == "work":
            self.work_counter += 1
            self.label["fg"] = "black"
        elif current_status == "break":
            self.label["fg"] = GREEN
        elif current_status == "long_break":
            self.label["fg"] = PINK

    def cycle_pomdoro_status(self, current_status, long_break_due):
        self.previous_pomodoro_status = current_status
        if current_status == "work":
            if long_break_due:
                new_status = "long_break"
            else:
                new_status = "break"
        else:
            new_status = "work"
        return new_status


    def reset(self):
        # soft reset - time of current session reset to start
        # or full reset (click reset twice in row) - reset of full module
        self.number_of_consecutive_reset_clicks += 1
        full_reset = self.number_of_consecutive_reset_clicks == 2
        soft_reset = not full_reset
        if full_reset:
            self.__init__()
        elif soft_reset:
            self.highest_timer_running += 1
            self.pomodoro_timer(self.previous_pomodoro_status)
        return











#runs tkinter
if __name__ == "__main__":
    app = App()
    app.mainloop()

