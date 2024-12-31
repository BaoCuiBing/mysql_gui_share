def handle_centering_win(win_widget):
    size = (win_widget.winfo_screenwidth(), win_widget.winfo_screenheight())
    win_size = (win_widget.winfo_width(), win_widget.winfo_height())
    win_widget.geometry(f"{win_size[0]}x{win_size[1]}+{size[0]//2 - win_size[0]//2}+{size[1]//2 - win_size[1]//2}")

def replace_multiple_placeholders(text, placeholder, values):
    for value in values:
        text = text.replace(placeholder, value, 1)
    return text

def sql_ping_jie_insert(table_name, ziduan_lists, zhi_lists):
    ziduan_lists = list(ziduan_lists)
    sql_juzi = f"INSERT INTO {table_name}({", ".join(ziduan_lists)}) VALUES ('{"', '".join(zhi_lists)}');"
    return sql_juzi

def sql_ping_jie_update(table_name, ziduan_lists, zhi_lists, row_id_ziduan_name, row_id):
    ziduan_lists = list(ziduan_lists)
    temp_juzi = ""
    for i in range(len(ziduan_lists)):
        temp_juzi += f"{ziduan_lists[i]} = '{zhi_lists[i]}'"
        if i != len(ziduan_lists)-1:
            temp_juzi += ", "
    sql_juzi = f"UPDATE {table_name} SET {temp_juzi} WHERE {row_id_ziduan_name} = {row_id};"
    return sql_juzi

def sql_ping_jie_del(table_name, id_ziduan_name, id_val):
    return f"DELETE FROM {table_name} WHERE {id_ziduan_name} = {id_val};"