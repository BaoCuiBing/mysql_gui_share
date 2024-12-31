import tkinter as old_tk
from tkinter import ttk as new_tk
from tkinter import messagebox
import asyncio
import config
import custom_functions.widget_components as widget_components
import custom_functions.sql_zhi_xing as sql_zhi_xing


class EditWindow(old_tk.Toplevel):
    def __init__(self, master=None, zu_jian={"tree_obj": None, "values": None, "edit_obj": None, "model": "",
                                             "item_id": None, "tables_name": ""}, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title(f'编辑记录------{zu_jian["model"]}')
        self.iconbitmap(config.WIN_ICON)
        self.config(width=600, height=480)
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        widget_components.handle_centering_win(self)

        self.tree_obj = zu_jian["tree_obj"]  # tree对象
        self.values = zu_jian["values"]
        self.cao_zuo_model = zu_jian["model"]
        self.item_id = zu_jian["item_id"]
        self.tables_name = zu_jian["tables_name"]

        self.column_key = zu_jian["edit_obj"]["column_key"]
        self.column_txt = zu_jian["edit_obj"]["column_txt"]

        self.self_entry_obj_dict = {}
        self.all_entry_vars_dict = {}

        for i in range(len(self.column_key)):
            self.all_entry_vars_dict[self.column_key[i]] = old_tk.StringVar()
            if len(self.values) != 0:
                self.all_entry_vars_dict[self.column_key[i]].set(self.values[i])
            new_tk.Label(self, text=self.column_txt[i]).grid(row=i, column=0, padx=10, pady=10)
            new_tk.Label(self, text=f"({self.column_key[i]})").grid(row=i, column=1, padx=10, pady=10)
            if self.column_key[i] in config.NOT_EDIT[self.tables_name][self.cao_zuo_model]:
                entry_state = "disabled"
            else:
                entry_state = "normal"
            self.self_entry_obj_dict[self.column_key[i]] = new_tk.Entry(self, textvariable=self.all_entry_vars_dict[self.column_key[i]],
                                                                        state=entry_state)
            self.self_entry_obj_dict[self.column_key[i]].grid(row=i, column=2, padx=10, pady=10)

        new_tk.Button(self, text="保存/更新数据", command=self.save_update_data).grid(row=len(self.column_key), column=1)

    def save_update_data(self):
        cheage_update_data = []
        for j in range(len(self.column_key)):
            cheage_update_data.append(self.all_entry_vars_dict[self.column_key[j]].get())
        id_zidaun_name = config.SQL_PEIZHI_DICTS[self.tables_name]["column_key"][0]
        all_key_list = config.SQL_PEIZHI_DICTS[self.tables_name]["column_key"]
        bu_fen_list = config.NOT_EDIT[self.tables_name][self.cao_zuo_model]
        kequ_ziduan_lists = [item for item in list(all_key_list)
                             if item not in list(bu_fen_list)]
        removed_indices = [index for index, item in enumerate(all_key_list) if item in bu_fen_list]
        kequ_values_lists = [item for index, item in enumerate(cheage_update_data) if index not in removed_indices]
        if self.cao_zuo_model == "update":
            sql_ju = widget_components.sql_ping_jie_update(self.tables_name, kequ_ziduan_lists, kequ_values_lists, id_zidaun_name, cheage_update_data[0])
            back_update_val = asyncio.run(sql_zhi_xing.running_transactions(sql_ju, "update"))
            if back_update_val[0] == False:
                messagebox.showerror("错误", f"更新数据失败： {back_update_val[1]}")
                return 0
            else:
                self.tree_obj.item(self.item_id, value=tuple(cheage_update_data))

        elif self.cao_zuo_model == "add":
            sql_ju = widget_components.sql_ping_jie_insert(self.tables_name, kequ_ziduan_lists, kequ_values_lists)
            back_add_val = asyncio.run(sql_zhi_xing.running_transactions(sql_ju, "insert"))
            if back_add_val[0] == False:
                messagebox.showerror("错误", f"写入数据失败： {back_add_val[1]}")
                return 0
            else:
                cheage_update_data = ["手动刷新查看" if item == "" else item for item in cheage_update_data]
                self.tree_obj.insert("", "end", values=tuple(cheage_update_data))
        self.destroy()