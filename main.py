from customtkinter import *
import time
import keyboard
from threading import *
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
settings = config["CONFIG"]

set_appearance_mode(settings["appearance_mode"])
set_default_color_theme(settings["color_theme"])

class Main(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x400")
        self.title("AFK holder")
        self.resizable(False, False)
        self.main()

    def main(self):
        self.input = CTkEntry(self, placeholder_text="interval in seconds")
        self.input.pack()
        self.input.place(x=280, y=100)

        self.startbtn = CTkButton(self, text="start", command=self.click_button_start)
        self.startbtn.pack()
        self.startbtn.place(x=280, y=130)

        self.button_to_press = CTkOptionMenu(self, values=["w", "a", "s", "d", "space"])
        self.button_to_press.pack()
        self.button_to_press.place(x=280, y=160)
        self.button_to_press.set("Select button")

        self.settings_button = CTkButton(self, text="settings", command=self.settings)
        self.settings_button.pack()
        self.settings_button.place(x=560, y=0)

    def settings(self):
        self.input.destroy()
        self.startbtn.destroy()
        self.button_to_press.destroy()
        self.settings_button.configure(text="main", command=self.close_settings)

        self.appearance_mode = CTkOptionMenu(self, values=["dark", "light", "system"], command=self.change)
        self.appearance_mode.pack()
        self.appearance_mode.set(settings["appearance_mode"])
        self.appearance_mode.place(x=280, y=160)

        self.color_theme = CTkOptionMenu(self, values=["blue", "dark-blue", "green"], command=self.change)
        self.color_theme.pack()
        self.color_theme.set(settings["color_theme"])
        self.color_theme.place(x=280, y=130)

    def change(self, mode):
        if mode == "dark" or mode == "light" or mode == "system":
            set_appearance_mode(mode)
            settings["appearance_mode"] = mode
            file = open("config.ini", "w")
            config.write(file)
        elif mode == "blue" or mode == "dark-blue" or mode == "green":
            set_default_color_theme(mode)
            settings["color_theme"] = mode
            file = open("config.ini", "w")
            config.write(file)

    def close_settings(self):
        self.settings_button.destroy()
        self.main()

    def click_button_start(self):
        thread = Thread(target=self.click_button)
        thread.start()
        self.running = True
        self.startbtn.configure(text="stop", command=self.stop)

    def stop(self):
        self.running = False
        self.startbtn.configure(text="start", command=self.click_button_start)

    def click_button(self):
        time.sleep(5)
        while self.running:
            keyboard.press(self.button_to_press.get())
            time.sleep(0.5)
            keyboard.release(self.button_to_press.get())
            time.sleep(int(self.input.get()))


if __name__ == "__main__":
    Main().mainloop()
