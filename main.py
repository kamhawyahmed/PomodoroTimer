import time
import tkinter as tk
from tkinter import ttk
#TODO START GUI
#colorhunt.co for color palettes
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
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
        self.attributes('-topmost',True)
        self.timer_running = False
        self.set_window_geometry()

        self.title("Pomodoro Timer")
        self.minsize(width=200, height=200)
        self.config(padx=10, pady=10, bg=YELLOW)
        ttk.Style(self).theme_use('classic') #no effect on mac
        # self.grid_columnconfigure(100)
        self.create_widgets()
        #TODO canvas positioning center and label etc.
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
        self.button_start = tk.Button(text="Start Timer", command=self.pomodoro_countdown, highlightbackground=YELLOW)
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
        self.label = tk.Label(text="25:00", font=("Arial", 40, "bold"), bg=YELLOW)
        if self.pomodoro_status == "break":
            self.label.config(fg=RED)
        # changing options - at init/as_dict/using.config fxn
        # my_label.config(text="New Label Text")
        # my_label.config(padx=25,pady=25)
        # self.label.pack(side="top", expand=False) #PACKER - display management
        # my_label.place(x=70,y=80)
        self.label.grid(column=0, columnspan=2, row=3)  # SNAPS TO TOP LEFT IF EMPTY ROW OR COLUMN IN BETWEEN

        self.label_checkmarks = tk.Label(text= "✓", font=("Arial", 24, "bold"), bg=YELLOW, fg=GREEN)
        # self.label_checkmarks.pack(side="top")
        self.label_checkmarks.grid(column=0, columnspan=2,row=4)


    def countdown_recursive(self, timer_length):
        if timer_length < 0:
            self.timer_running = False
            return

        minutes, seconds = convert_seconds_to_minutes(timer_length)
        self.label["text"] = f"{minutes}:{seconds}"
        self.after(1000, self.countdown_recursive, timer_length - 1)


    def pomodoro_countdown(self):
        #TODO change text color based on status red - work, green - break or long break
        #TODO have skip to next timer if button pressed again
        print(self.pomodoro_status)
        if self.timer_running:
            print("timer in progress")
        self.timer_running = True

        if self.work_counter == 4:
            self.pomodoro_status = "long break"
            self.countdown_recursive(LONG_BREAK_MIN * 60)
            self.work_counter = 0
            self.pomodoro_status = "work"
        elif self.pomodoro_status == "work":
            self.countdown_recursive(2)
            self.work_counter += 1
            self.pomodoro_status = "break"
        elif self.pomodoro_status == "break":
            self.countdown_recursive(SHORT_BREAK_MIN * 60)
            self.pomodoro_status = "work"
        else:
            raise NameError("Pomodoro status not set correctly.")
    def reset(self):
        return











#runs tkinter
if __name__ == "__main__":
    app = App()
    app.mainloop()

#TODO GUI BUTTONS (RESPONSES TO PRESS)

#TODO TIMER

#TODO MAKE PRETTY

