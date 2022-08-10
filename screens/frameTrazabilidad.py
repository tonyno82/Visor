import tkinter as tk

class FrameTraza(tk.Frame):
    def __init__(self, contenedor):
        super().__init__(contenedor)
        self.configure(background='#fcba03', height=980, width=1280)
        self.boton = tk.Button(self, text='Punsar').grid()