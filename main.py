import tkinter as old_tk
from tkinter import ttk as new_tk
from tkinter import messagebox
import custom_functions.widget_components as widget_components
import config

import pages.data_init as data_init
import pages.more_table_frame as more_table_frame

class main():
    def __init__(self):
        self.main_win = old_tk.Tk()
        self.main_win.title("MySQL作业GUI (代码这么多)")
        self.main_win.resizable(False, False)
        self.main_win.geometry("1200x900")
        print(config.WIN_ICON)
        self.main_win.iconbitmap(config.WIN_ICON)
        widget_components.handle_centering_win(self.main_win)
        
        self.NewWeghtWindow = None   # 存放窗口对象

        self.login_txt_val = old_tk.StringVar()
        self.login_txt_val.set("登录")
        login_user_button = new_tk.Button(self.main_win, textvariable=self.login_txt_val, command=lambda:self.open_win("login_win"))
        login_user_button.place(x=10, y=5)

        self.father_note_frame = new_tk.Notebook(width=1200, height=850)
        self.father_note_frame.place(x=0, y=50)
        self.father_note_frame.bind("<<NotebookTabChanged>>", self.cheage_notebook)

        self.data_init_frame = data_init.MySsqlInitFrame(self.father_note_frame)
        self.father_note_frame.add(self.data_init_frame, text="数据库初始化")

        self.user_frame = more_table_frame.TreeViewAllFrame(self.father_note_frame, zu_jian={"tables_name": "users"})
        self.father_note_frame.add(self.user_frame, text="用户数据")
        self.taiqiu_dark_frame = more_table_frame.TreeViewAllFrame(self.father_note_frame, zu_jian={"tables_name": "tables"})
        self.father_note_frame.add(self.taiqiu_dark_frame, text="台球桌数据")
        self.yuding_frame = more_table_frame.TreeViewAllFrame(self.father_note_frame, zu_jian={"tables_name": "reservations"})
        self.father_note_frame.add(self.yuding_frame, text="预定信息")
        self.jiaoyi_pay_frame = more_table_frame.TreeViewAllFrame(self.father_note_frame, zu_jian={"tables_name": "transactions"})
        self.father_note_frame.add(self.jiaoyi_pay_frame, text="交易记录表")
        self.wei_xiu_frame = more_table_frame.TreeViewAllFrame(self.father_note_frame, zu_jian={"tables_name": "maintenance_logs"})
        self.father_note_frame.add(self.wei_xiu_frame, text="维修日志")

        self.jian_ce_user()

        self.main_win.mainloop()

    def jian_ce_user(self):
        if config.login_user == {}:
            self.father_note_frame.place_forget()
        else:
            self.father_note_frame.place(x=0, y=50)

    def open_win(self, win_type):
        if win_type == "login_win":
            if config.login_user == {}:
                from pages.login_win import LoginWindow as top_win
                self.NewWeghtWindow = top_win(self.main_win,{"log_user_name": self.login_txt_val, "over_zhixin": self.jian_ce_user})
            else:
                quren_win = messagebox.askyesno("退出登录", "退出登录吗？")
                if quren_win:
                    config.login_user = {}
                    self.login_txt_val.set("登录")
                    self.NewWeghtWindow = None
                    self.jian_ce_user()

    def cheage_notebook(self, event):
        notebook = event.widget
        selected_tab = notebook.select()
        tab_index = notebook.index(selected_tab)
        if tab_index == 1:  # 用户管理
            self.user_frame.sel_all_data()
        elif tab_index == 2:
            self.taiqiu_dark_frame.sel_all_data()
        elif tab_index == 3:
            self.yuding_frame.sel_all_data()
        elif tab_index == 4:
            self.jiaoyi_pay_frame.sel_all_data()
        elif tab_index == 5:
            self.wei_xiu_frame.sel_all_data()




if __name__ == '__main__':
    main()

