from pymysql.err import MySQLError
import aiomysql
import asyncio
import pprint
import config


async def sql_link_content(mysql_link_data):  # 创建连接池
    yi_bu_content = await aiomysql.create_pool(
        host=mysql_link_data["host"],
        port=mysql_link_data["port"],
        user=mysql_link_data["user"],
        password=mysql_link_data["password"],
        db=mysql_link_data["db"],
        charset='utf8mb4',
        autocommit=True,
        maxsize=10,
        minsize=1
    )
    return yi_bu_content

async def sql_zhi_xing(content, sql_sentence, type="select"):   # content表示连接池对象
    async with content.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql_sentence)
            if type == "select":
                result = await cursor.fetchall()
                print("查询成功")
                return result
            elif type == "insert" or type == "update" or type == "delete":
                if cursor.rowcount > 0:
                    print(f"成功影响{cursor.rowcount}行数据")
                    return True
                else:
                    return False

async def running_transactions(sql_juzi, caozuo_type):
    content = await sql_link_content(config.MYSQL_LINK_CONFIG)
    try:
        back_val = await sql_zhi_xing(content, sql_juzi, type=caozuo_type)
        return back_val, "yes"
    except MySQLError as err:
        print(err)
        return False, f"{err}"
    finally:
        content.close()
        await content.wait_closed()


# back_val = asyncio.run(running_transactions("SELECT * FROM users WHERE phone='13634567890' AND password= '23dj890k';", "select"))
# print(back_val[0][0])
# print(back_val[1])
