import tkinter as old_tk
from tkinter import ttk as new_tk


class MySsqlInitFrame(new_tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.config(width=1200, height=850)

        old_tk.Label(self, text="这个功能逻辑太绕，没写Over，不show", font=("微软雅黑", 30), fg="#cbd0db").pack(expand=True, fill="both")