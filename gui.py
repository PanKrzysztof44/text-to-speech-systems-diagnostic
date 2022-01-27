from time import sleep
from pickle import TRUE
import tkinter as tk
from tkinter import messagebox
from pytts import TTS

FONT_NAME = "Arial"
MAIN_LABEL_FONT_SIZE = 20
CONF_LABEL_FONT_SIZE = 14
ENTRY_FONT_SIZE = 14
BUTTON_FONT_SIZE = 14
RADIOBUTTON_FONT_SIZE = 14

ENTRY_WIDTH = 50
ENTRY_HEIGHT = 5

BUTTON_WIDTH = 40
BUTTON_HEIGHT = 10


class ttsGUI:
    def __init__(self, master):

        # text to speech class
        self.tts = TTS()

        self.master = master
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        self.master.title("Text to speech GUI")

        self.frame = tk.Frame(master)
        self.frame.grid(row=0, column=0)

        self.text_var = tk.StringVar(self.frame, value="")

        main_label_text = "Write any text you want, then click 'Speak!' button to start text to speech conversion"
        self.main_app_label = tk.Label(
            self.frame, text=main_label_text, font=(
                FONT_NAME, CONF_LABEL_FONT_SIZE)
        )

        self.text_input = tk.Text(
            self.frame,
            font=(FONT_NAME, ENTRY_FONT_SIZE),
            width=ENTRY_WIDTH,
            height=ENTRY_HEIGHT,
        )

        self.speek_button = tk.Button(
            self.frame,
            text="Speak!",
            command=self.speak,
            font=(FONT_NAME, BUTTON_FONT_SIZE),
        )

        self.main_app_label.grid(row=1, column=1, padx=(10, 10), pady=(10, 10))

        self.text_input.grid(row=2, column=1, pady=(10, 10))

        self.speek_button.grid(row=3, column=1, pady=(10, 10))

        self.view = False

    def speak(self):
        self.tts.text_to_speech(self.retrieve_input())

    def retrieve_input(self):
        return self.text_input.get("1.0", 'end-1c')


if __name__ == "__main__":
    root = tk.Tk()
    my_gui = ttsGUI(root)
    root.mainloop()
