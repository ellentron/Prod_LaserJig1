import tkinter as tk
from tkinter import ttk


class GUI:
    def __init__(self, master, start_test_callback, pause_test_callback, stop_test_callback):
        self.start_test_callback = start_test_callback
        self.pause_test_callback = pause_test_callback
        self.stop_test_callback = stop_test_callback

        self.master = master
        self.master.title("Test UI")
        self.master.geometry("300x250")

        self.button_start = ttk.Button(self.master, text="Start Test", command=self.start_test_callback)
        self.button_pause = ttk.Button(self.master, text="Pause Test", command=self.pause_test_callback)
        self.button_stop = ttk.Button(self.master, text="Stop Test", command=self.stop_test_callback)

        self.button_start.pack()
        self.button_pause.pack()
        self.button_stop.pack()


