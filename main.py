import sys
import datetime as dt
import tkinter as tk
from tkinter import ttk
import os
import database_module as db
#colorhunt.co for color palettes
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
ORANGE = "#EBA487"
YELLOW = "#f7f5dd"
SKY_BLUE = "#87CEEB"
LIGHT_BLUE = "#48B3DF"

WIDTH_PROGRAM = 225
TOTAL_NUMBER_COLUMNS = 3

TEST_ROW = 0
FIRST_ROW = TEST_ROW + 1
SECOND_ROW = FIRST_ROW + 1
THIRD_ROW = SECOND_ROW + 1
FOURTH_ROW = THIRD_ROW + 1
FIFTH_ROW = FOURTH_ROW + 1

FONT_NAME = "Courier"
NUMBER_OF_SESSIONS_BEFORE_LONG_BREAK = 4
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

#for pyinstaller deployment of images - use resource_path(filename) instead of file names
#- adding image as data file not working for me but making mac apps so can just add to MacOS folder in package contents
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
###
def convert_seconds_to_minutes(seconds):
    minutes, seconds = divmod(seconds, 60)
    return minutes, seconds

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.pomodoro_status = "work"
        self.work_counter = 0
        self.timer_running = False
        self.highest_timer_running = 0 #actually starts at 1, incrementation before implementation
        self.number_of_consecutive_reset_clicks = 0
        self.previous_pomodoro_status = ""
        self.db = db.DatabaseManager() #poor form - copying meditechprinter aidan but wtv

        self.start_time = None
        self.paused = False
        self.current_timer_characteristics = []

        self.attributes('-topmost',True)
        self.title("Pomodoro Timer")
        # photo = tk.PhotoImage(file="tomato.png")
        # self.iconphoto(True, photo)
        self.minsize(width=WIDTH_PROGRAM, height=100)
        self.config(padx=10, pady=10, bg=YELLOW)
        ttk.Style(self).theme_use('classic') #no effect on mac
        self.set_window_geometry_bottom_right()
        self.create_widgets()

    def set_window_geometry_bottom_right(self):
        print("bottom right")
        w = WIDTH_PROGRAM  # width for the Tk root
        h = 60  # height for the Tk root

        # get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws * 92 / 100) - (w / 2)
        y = (hs * 80 / 100) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.geometry(f"{w}x{h}+{int(x)}+{int(y)}")

    def set_window_position_middle(self):
        w = WIDTH_PROGRAM  # width for the Tk root
        h = 220  # height for the Tk root

        # get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws * 1 / 2) - (w / 2)
        y = (hs * 1 / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
    def create_widgets(self):
        #TODO STOP ADDING PREFERENCES AS TODO

        # self.button_test = tk.Button(text="TEST", command=self.pause_unpause_button_pressed, highlightbackground=YELLOW, )
        # self.button_test.grid(column=0, row=TEST_ROW)
        # self.button_test2 = tk.Button(text="TEST", command=self.unpause_timer, highlightbackground=YELLOW, )
        # self.button_test2.grid(column=1, row=TEST_ROW)

        self.button_pause = tk.Button(text="Pause", command=self.pause_unpause_button_pressed, highlightbackground=YELLOW, )
        self.button_pause.grid(column=1, row=SECOND_ROW, pady= (0,10))
        # self.button_pause.config(width= , height=0, font=("Arial", 28, "bold"))
        # ⏸

        self.button_start = tk.Button(text="Start", command=self.pomodoro_button_pressed, highlightbackground=YELLOW,)
        # self.button_start.pack(side="left")
        self.button_start.grid(column=0, row=SECOND_ROW, pady= (0,10))

        self.button_reset = tk.Button(text="Reset", command=self.reset, highlightbackground=YELLOW)
        # self.button_reset.pack(side="left", padx=30)
        self.button_reset.grid(column=2,row=SECOND_ROW, pady= (0,10))


        # self.canvas = tk.Canvas(width=180, height=79, bg=YELLOW, highlightthickness=0)
        self.image = tk.PhotoImage(file=resource_path("tomato.png"))
        # self.canvas.create_image(90,39, image=self.image) #position relative to canvas
        # self.canvas.create_text(120,86, text="25:00", font=("Arial", 40, "bold"), fill="black")

        # self.canvas.pack(side="top")
        # self.canvas.grid(column=0, columnspan=2, row=2)
        # Text Label
        minutes, seconds = convert_seconds_to_minutes(WORK_MIN * 60)

        self.label = tk.Label(text= f"{minutes:>02}:{seconds:>02}".format(number=4), font=("Arial", 40, "bold"), bg=YELLOW, fg= "black")
        # self.label.bind('<Double-Button-1>', self.setup_editable_label)
        # self.label.bind('<Enter>', self.setup_editable_label)

        # changing options - at init/as_dict/using.config fxn
        # my_label.config(text="New Label Text")
        # my_label.config(padx=25,pady=25)
        # self.label.pack(side="top", expand=False) #PACKER - display management
        # my_label.place(x=70,y=80)
        self.label.grid(column=0, columnspan=TOTAL_NUMBER_COLUMNS, row=FIRST_ROW)  # SNAPS TO TOP LEFT IF EMPTY ROW OR COLUMN IN BETWEEN
        self.label_start_time = tk.Label(text= f"Start: ", font=("Arial", 18, "bold"), bg=YELLOW, fg="black")
        self.label_start_time.grid(column=0, columnspan=TOTAL_NUMBER_COLUMNS,row=THIRD_ROW)
        self.label_elapsed_time = tk.Label(text= f"Elapsed: ", font=("Arial", 18, "bold"), bg=YELLOW, fg="black")
        self.label_elapsed_time.grid(column=0, columnspan=TOTAL_NUMBER_COLUMNS,row=FOURTH_ROW)



        self.label_checkmarks = tk.Label(text= "✓", font=("Arial", 24, "bold"), bg=YELLOW, fg=GREEN)
        # self.label_checkmarks.pack(side="top")
        self.label_checkmarks.grid(column=0, columnspan=3,row=FIFTH_ROW)


    def setup_editable_label(self, event):
        self.label["fg"] = "white"
        # self.label["text"] =
        print(event)
    def countdown_recursive(self, timer_length_seconds, id_number, original_timer_length):
        #for future reference - can assign recursive function to name and use tk.window.after_cancel to cancel
        self.timer_running = True
        self.current_timer_characteristics = {"Timer_Length": timer_length_seconds, "ID_Number": id_number,
                                              "Original_Timer_Length": original_timer_length}
        if timer_length_seconds < 0:
            self.set_window_position_middle()
            self.update_checkmarks()
            self.timer_running = False
            return

        if id_number < self.highest_timer_running or self.highest_timer_running == 0:
            self.timer_running = False
            return

        if self.paused:
            self.timer_running = False
            return



        minutes, seconds = convert_seconds_to_minutes(timer_length_seconds)
        self.label["text"] = f"{minutes:>02}:{seconds:>02}"
        self.label_elapsed_time["text"] = f"Elapsed: {self.calculate_elapsed_time(current_time=dt.datetime.now())}"


        self.current_timer_identifier = self.after(1000, self.countdown_recursive, timer_length_seconds - 1, id_number, original_timer_length)


    def calculate_elapsed_time(self, current_time, start_time=None):
        if start_time == None:
            start_time = self.start_time
        elapsed_time = current_time - start_time
        elapsed_time_formatted = str(elapsed_time).split(".")[0]
        return elapsed_time_formatted

    def pomodoro_button_pressed(self):
        #the levels of this function are mismatched - update checkmarks
        # #consecutivereset should be in different place than work timer and work effects
        self.set_window_geometry_bottom_right()
        self.update_checkmarks()
        self.number_of_consecutive_reset_clicks = 0
        self.unpause_timer()


        self.highest_timer_running += 1

        if self.work_counter == 0:
            self.start_time = dt.datetime.now()
            self.db.data["Start_Time"] = self.start_time

            self.label_start_time["text"] = f'Start: {self.start_time.strftime("%I:%M %p")}'


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
    def change_all_backgrounds(self, background_color):
        # self.canvas.config(bg=background_color)
        # self.button_test.config(highlightbackground=background_color)
        # self.button_test2.config(highlightbackground=background_color)
        self.button_pause.config(highlightbackground=background_color)
        self.label_elapsed_time.config(bg=background_color)
        self.label_start_time.config(bg=background_color)
        self.config(bg=background_color)
        self.label.config(bg=background_color)
        self.label_checkmarks.config(bg=background_color)
        self.button_start.config(highlightbackground=background_color)
        self.button_reset.config(highlightbackground=background_color)
    def apply_extra_effects(self, current_status):
        if current_status == "work":
            self.work_counter += 1
            self.label["fg"] = "black"
            self.change_all_backgrounds(ORANGE)
        elif current_status == "break":
            self.change_all_backgrounds(LIGHT_BLUE)
            # self.label["fg"] = GREEN
        elif current_status == "long_break":
            self.change_all_backgrounds(LIGHT_BLUE)
            # self.label["fg"] = PINK

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

    def pause_unpause_button_pressed(self):
        self.number_of_consecutive_reset_clicks = 0
        if not self.paused:
            self.pause_timer()
        else:
            self.unpause_timer()
        return
    def pause_timer(self):
        self.paused = True
        self.label["fg"] = "white"
        return
    def unpause_timer(self):
        print(self.current_timer_characteristics)
        self.paused = False
        self.label["fg"] = "black"
        self.highest_timer_running += 1
        if self.current_timer_characteristics:
            self.countdown_recursive(self.current_timer_characteristics["Timer_Length"], self.highest_timer_running,
                                    self.current_timer_characteristics["Original_Timer_Length"])
        self.current_timer_characteristics = []
        return


    def reset(self):
        # soft reset - time of current session reset to start
        # or full reset (click reset twice in row) - reset of full module
        self.number_of_consecutive_reset_clicks += 1
        full_reset = self.number_of_consecutive_reset_clicks == 2
        soft_reset = not full_reset
        if full_reset:
            self.collect_end_data()
            self.save_all_data_to_csv()
            self.destroy()
            self.__init__()
        elif soft_reset:
            self.unpause_timer()
            self.highest_timer_running += 1
            self.pomodoro_timer(self.previous_pomodoro_status)
            self.pause_timer()
        return
    def collect_end_data(self):
        self.db.data["Sessions_Worked"] = self.work_counter
        self.db.data["Minutes_Worked"] = self.work_counter * WORK_MIN
        self.db.data["End_Time"] = dt.datetime.now()
    def save_all_data_to_csv(self):
        self.db.append_memory_to_csv()




#runs tkinter
if __name__ == "__main__":
    app = App()
    app.mainloop()

