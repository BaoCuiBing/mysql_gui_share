import tkinter as old_tk
from tkinter import ttk as new_tk
from tkinter import messagebox
import asyncio
import config
import custom_functions.widget_components as widget_components
import custom_functions.sql_zhi_xing as sql_zhi_xing


class LoginWindow(old_tk.Toplevel):
    def __init__(self, master=None, zu_jian={}, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title('登录')
        self.iconbitmap(config.WIN_ICON)
        self.config(width=400, height=480)
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        widget_components.handle_centering_win(self)

        self.zu_jian = zu_jian

        self.user_num_val = old_tk.StringVar()
        self.password_num_val = old_tk.StringVar()

        new_tk.Label(self, text="账号/电话：").grid(row=0, column=0, padx=5, pady=5)
        new_tk.Label(self, text="密码：").grid(row=1, column=0, padx=5, pady=5)
        self.user_num = new_tk.Entry(self, textvariable=self.user_num_val)
        self.user_num.grid(row=0, column=1, padx=5, pady=5)
        self.password = new_tk.Entry(self, textvariable=self.password_num_val)
        self.password.grid(row=1, column=1, padx=5, pady=5)

        new_tk.Button(self, text="登录", command=self.login_dong_zuo).grid(row=2, padx=15, pady=20)

    def login_dong_zuo(self):
        sql_juzi = f"SELECT * FROM users WHERE phone = '{self.user_num_val.get()}' AND password = '{self.password_num_val.get()}';"
        back_login_val = asyncio.run(sql_zhi_xing.running_transactions(sql_juzi, "select"))
        if len(back_login_val[0]) != 0:
            config.login_user = back_login_val[0][0]
            self.zu_jian["log_user_name"].set(f"用户名：{config.login_user[1]}（单击退出登录）")
            self.zu_jian["over_zhixin"]()
            self.destroy()
        else:
            messagebox.showinfo("提示", "账号（电话号）密码错误", master=self)