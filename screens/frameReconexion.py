import tkinter as tk

class FrameReconexion(tk.Frame):
    def __init__(self, manager):
        super().__init__(manager)
        self.configure(background='#03ecfc', height=980, width=1280)