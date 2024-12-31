import os

login_user = {}   # 用户登录信息

MYSQL_LINK_CONFIG = {
    'host': '47.120.20.224',
    'port': 3306,
    'user': "root",
    'password': "6ba72c88eb932e1c",
    'db': "PoolHallManagement"
}

SQL_PEIZHI_DICTS = {
    "users": {"column_key": ("user_id", "name", "phone", "password", "role", "created_at"),
            "column_txt": ("用户ID", "用户姓名", "账号（联系电话）", "密码", "角色类型", "注册时间")},
    "tables": {"column_key": ("table_id", "table_number", "status", "hourly_rate"),
            "column_txt": ("球桌ID", "球桌编号", "球桌状态", "每小时收费金额")},
    "reservations": {"column_key": ("reservation_id", "user_id", "table_id", "start_time", "end_time", "total_fee"),
            "column_txt": ("预订ID", "顾客ID", "球桌ID", "预订开始时间", "预订结束时间", "总费用")},
    "transactions": {"column_key": ("transaction_id", "user_id", "reservation_id", "amount", "payment_time", "payment_method"),
            "column_txt": ("交易ID", "顾客ID", "预订ID", "支付金额", "支付时间", "支付方式")},
    "maintenance_logs": {"column_key": ("log_id", "table_id", "staff_id", "maintenance_date", "details"),
            "column_txt": ("日志ID", "球桌ID", "员工ID", "维修日期", "维修详情")}
}

NOT_EDIT = {
    "users": {
        "update": ["user_id"],
        "add": ["user_id", "created_at"]
    },
    "tables": {
        "update": ["table_id"],
        "add": ["table_id"]
    },
    "reservations": {
        "update": ["reservation_id"],
        "add": ["reservation_id"]
    },
    "transactions": {
        "update": ["transaction_id"],
        "add": ["transaction_id", "payment_time"]
    },
    "maintenance_logs": {
        "update": ["log_id"],
        "add": ["log_id"]
    }
}

current_file_path_os = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(current_file_path_os).replace("\\", "/")+"/"

WIN_ICON = CURRENT_DIR + "src/imgs/mysql_zuo_ye.ico"

