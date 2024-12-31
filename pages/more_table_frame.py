import pprint
import tkinter as old_tk
from tkinter import ttk as new_tk
from tkinter import messagebox

import config
import custom_functions.sql_zhi_xing as sql_zhi_xing
import custom_functions.widget_components as widget_components
import asyncio


class TreeViewAllFrame(new_tk.Frame):
    def __init__(self, master=None, zu_jian={"tables_name": ""}, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.config(width=1200, height=850)

        self.left_frame = new_tk.Frame(self, width=940, height=850)
        self.left_frame.place(x=0, y=0)
        self.left_frame.pack_propagate(False)

        self.zu_jian = zu_jian

        self.shuju_data = config.SQL_PEIZHI_DICTS[zu_jian["tables_name"]]
        self.gezi_width = 940 // len(self.shuju_data["column_key"])

        self.tree = new_tk.Treeview(self.left_frame, columns=self.shuju_data["column_key"], show="headings")
        for i in range(len(self.shuju_data["column_key"])):
            self.tree.heading(self.shuju_data["column_key"][i], text=self.shuju_data["column_txt"][i])
            self.tree.column(self.shuju_data["column_key"][i], anchor="center", width=self.gezi_width)

        self.data = []
        self.WinObject = None

        scrollbar = new_tk.Scrollbar(self.left_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(expand=True, fill="y")
        self.tree.bind("<Button-3>", self.show_menu)  # 绑定右键

        self.menu = old_tk.Menu(self.left_frame, tearoff=0)
        self.menu.add_command(label="修改", command=lambda: self.edit_data_item())
        self.menu.add_command(label="删除", command=lambda: self.delete_data_item())


        self.right_frame = new_tk.Frame(self, width=260, height=850)
        self.right_frame.place(x=941, y=0)
        self.right_frame.pack_propagate(False)

        new_tk.Button(self.right_frame, text="添加记录", command=self.add_data_item).place(x=10, y=20)
        new_tk.Button(self.right_frame, text="手动刷新数据表", command=self.sel_all_data).place(x=10, y=60)

    def show_menu(self, event):  # 右击菜单
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.menu.post(event.x_root, event.y_root)

    def sel_all_data(self):   # 获取数据
        self.clear_data()
        sql_juzi = f"SELECT * FROM {self.zu_jian["tables_name"]};"
        back_user_val = asyncio.run(sql_zhi_xing.running_transactions(sql_juzi, "select"))
        back_user_val = back_user_val[0]
        if len(back_user_val[0]) != 0:
            self.data = back_user_val
            pprint.pprint(self.data)
            self.tree.delete()
            for row in self.data:
                self.tree.insert("", "end", values=row)

    def clear_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def edit_data_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = selected_item[0]
            values = self.tree.item(item, "values")
            from pages.edit_data_win import EditWindow as EditWindow
            self.WinObject = EditWindow(self, zu_jian={"tree_obj": self.tree, "values": values, "edit_obj": self.shuju_data,
                                                       "model": "update", "item_id": item, "tables_name": self.zu_jian["tables_name"]})

    def add_data_item(self):
        from pages.edit_data_win import EditWindow as EditWindow
        self.WinObject = EditWindow(self,zu_jian={"tree_obj": self.tree, "values": (), "edit_obj": self.shuju_data,
                                                  "model": "add", "item_id": None, "tables_name": self.zu_jian["tables_name"]})

    def delete_data_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = selected_item[0]
            id_value = self.tree.item(item, "values")[0]
            confirm = messagebox.askyesno("确认删除", "确定删除该条记录吗？")
            if confirm:
                sql_ju = widget_components.sql_ping_jie_del(self.zu_jian["tables_name"],
                                                            config.SQL_PEIZHI_DICTS[self.zu_jian["tables_name"]]["column_key"][0],
                                                            id_value)
                back_del_val = asyncio.run(sql_zhi_xing.running_transactions(sql_ju, "insert"))
                if back_del_val[0] == False:
                    messagebox.showerror("错误", f"删除数据失败： {back_del_val[1]}")
                    return 0
                else:
                    self.tree.delete(item)

    def select_data_item(self):
        pass
