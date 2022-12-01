import random
from tkinter import *
import csv

# Constants
BEGINNING_BACKGROUND_COLOR = "#00BFFF"
TYPING_BACKGROUND_COLOR = "#FF6347"
RESULTS_BACKGROUND_COLOR = "#7FFF00"
SAMPLE_TEXT = "hello world these are some example words"
LARGE_FONT = ("Helvetica", 32, "bold")
SMALL_FONT = ("Helvetica", 20, "bold")
STARTING_TEXT = "Click Start To Begin"
RESULTS_TEXT = "↑ Here Are Your Final Results ↑"
TYPE_BELOW_TEXT = "↓ Type Using the Bar Below ↓"
UNDERLINE_TEXT = "The Word You Need To Type Will Be " + "\u0332".join("Underlined!")
timer = None
CHECK_WORD = 0

# Variables for handling words
# All words from our csv file
words_data = []
# Words that appear on screen in a string format
displayed_words = ""
# List of the current words on screen
on_screen_words = []
# Words that the user is typing from words_on_screen
typed_words = []
# List of all the words that have been typed
completed_words = []

# Reads our csv file and enters the words to our words_data list
with open("words.csv", encoding="utf-8") as words_list:
    data = csv.reader(words_list)
    for row in data:
        words_data.append(''.join(row))


# Functions
def random_words():
    """Generates new words to display and compare"""
    global displayed_words, completed_words, words_data, on_screen_words, typed_words
    displayed_words = ""
    on_screen_words = []
    typed_words = []
    for i in range(6):
        if len(displayed_words) >= 40:
            pass
        else:
            random_word = random.choice(words_data)
            if i == 0:
                displayed_words += "\u0332".join(random_word) + " "
            else:
                displayed_words += (random_word + " ")
            on_screen_words.append(random_word)
            words_data.remove(random_word)
    text_display["text"] = displayed_words


def user_typing(event):
    """Adds user typed words to the appropriate list if they match the required word. Also underlines the next
    word in sequence. If user has typed all the words on screen, random_words gets called"""
    global CHECK_WORD
    if user_input.get().strip() != on_screen_words[CHECK_WORD]:
        user_input.delete(0, "end")
    else:
        typed_words.append(user_input.get().strip())
        completed_words.append(user_input.get().strip())
        user_input.delete(0, "end")
        CHECK_WORD += 1
        if len(on_screen_words) == len(typed_words):
            CHECK_WORD = 0
            random_words()
        else:
            reassembled_string = ""
            for word in on_screen_words:
                if on_screen_words[CHECK_WORD] == word:
                    reassembled_string += "\u0332".join(word) + " "
                else:
                    reassembled_string += word + " "
            text_display["text"] = reassembled_string


def calculate_wpm_and_cpm():
    """calculates the words per minute and characters per minute from the completed words list"""
    wpm_display["text"] = f"WPM: {len(completed_words)}"
    string_form = ""
    for word in completed_words:
        string_form += word
    cpm_display["text"] = f"CPM: {len(string_form)}"


# Functions for timers
def countdown(count):
    """Main timer method for this program."""
    global timer
    timer = root.after(1000, countdown, count-1)
    if count < 10:
        count = f"0{count}"
    timer_display["text"] = count
    if count == "00":
        calculate_wpm_and_cpm()
        root.config(bg=RESULTS_BACKGROUND_COLOR)
        root.unbind("<space>")
        text_display["text"] = RESULTS_TEXT
        stop_timer()


def stop_timer():
    """Stops the timer"""
    root.after_cancel(timer)


def start_timer():
    """Starts timer and typing test"""
    underline_warning.place_forget()
    root.config(bg=TYPING_BACKGROUND_COLOR)
    root.bind("<space>", user_typing)
    start_button["state"] = "disabled"
    random_words()
    countdown(60)


# Reset Function
def reset():
    """Resets everything to its initial settings"""
    global timer, displayed_words, on_screen_words, typed_words, completed_words
    root.unbind("<space>")
    start_button["state"] = "normal"
    underline_warning.place(x=15, y=150)
    root.after_cancel(timer)
    timer_display["text"] = 60
    text_display["text"] = STARTING_TEXT
    root.config(bg=BEGINNING_BACKGROUND_COLOR)
    wpm_display["text"] = "WPM: ?"
    cpm_display["text"] = "CPM: ?"
    timer = None
    displayed_words = ""
    on_screen_words = []
    typed_words = []
    completed_words = []



# Creates Window
root = Tk()
root.title("Speed Typing Test")
root.geometry("750x500")
root.config(bg=BEGINNING_BACKGROUND_COLOR, padx=50, pady=50)

# Tkinter Widgets
timer_display = Label()
timer_display.config(bg="white", text=60, borderwidth=3, relief="solid", font=LARGE_FONT)
timer_display.place(x=100, y=5)

wpm_display = Label()
wpm_display.config(bg="white", text="WPM: ?", borderwidth=3, relief="solid", font=LARGE_FONT)
wpm_display.place(x=250, y=5)

cpm_display = Label()
cpm_display.config(bg="white", text="CPM: ?", borderwidth=3, relief="solid", font=LARGE_FONT)
cpm_display.place(x=450, y=5)

text_display = Label()
text_display.config(bg="white", borderwidth=3, text=STARTING_TEXT, relief="solid", font=SMALL_FONT)
text_display.place(x=10, y=100, width=650)

type_below = Label()
type_below.config(bg="white", borderwidth=3, relief="solid", font=SMALL_FONT, text=TYPE_BELOW_TEXT)
type_below.place(x=155, y=200)

underline_warning = Label()
underline_warning.config(bg="white", borderwidth=3, relief="solid", font=SMALL_FONT, text=UNDERLINE_TEXT)
underline_warning.place(x=15, y=150)

user_input = Entry()
user_input.config(bg="white", borderwidth=3, relief="solid", font=SMALL_FONT)
user_input.place(x=150, y=250, width=400, height=60)

start_button = Button()
start_button.config(bg="White", text="Start", borderwidth=3, relief="solid", font=SMALL_FONT, command=start_timer)
start_button.place(x=50, y=250)

reset_button = Button()
reset_button.config(bg="White", text="Reset", borderwidth=3, relief="solid", font=SMALL_FONT, command=reset)
reset_button.place(x=250, y=350)

# Mainloop to run window
root.mainloop()

