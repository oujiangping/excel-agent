"""
**************************************
*  @Author  ：   oujiangping
*  @Time    ：   2025/4/15 14:39
*  @FileName:   excel_tool.py
**************************************
"""
import io

from pandasql import sqldf

sheets_db = {}  # {sheet_name: DataFrame}


def is_regular_table(df):
    # markdown_text = df.to_markdown()
    # print(markdown_text)
    if df.empty:
        print(f"包含空表")
        return False

    # 取出第一行
    columns = df.columns.tolist()
    print(columns)
    # 确保不包含 Unnamed
    if any('Unnamed' in col for col in columns):
        print(f"包含Unnamed列")
        return False

    return True


def get_all_table_names(db):
    """获取所有已加载的表名（工作表名）"""
    return list(db.keys())


def get_excel_description(df):
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    buffer.close()
    return info_str


def get_excel_info_head(db):
    description = ""
    # 获取表结构描述
    # 将字典中的 DataFrame 分配变量名（例如表名）
    for sheet_name, df in db.items():
        info_str = get_excel_description(df)
        head_str = df.head().to_csv(sep='\t', na_rep='nan')
        item_str = f"表格结构描述：\n表名:{sheet_name}\n{info_str}\n\n前几行数据(不是全部数据，数据应该单独执行sql查询，请勿直接用于计算最终结果)：\n{head_str}\n\n----------------\n\n"
        description += item_str
    return description


async def run_sql_queries(queries: list[str]):
    """
    批量执行 SQL 查询并返回结果。
    参数:
    queries (str): 要执行的 SQL 查询语句列表。
    返回:
    返回序列化的执行结果
    """
    global sheets_db
    results = ""
    for query in queries:
        try:
            # 替换换行符为空格
            # query = query.replace('\\\n', ' ')
            print(f"执行 SQL 查询: {query}")
            sql_result = sqldf(query, get_global()).to_csv(sep='\t', na_rep='nan')
            results += f"query: {query}, result: {sql_result}\n\n----------"
        except Exception as e:
            print(f"执行 SQL 查询时出错: {e}")
            results += f"query: {query}, result: 执行 SQL 查询时出错。{e}\n\n----------"
    return results


def get_excel_info_tool():
    """
    获取表格结构和示例数据
    返回:
    str: 获取表格结构和示例数据。
    """
    global sheets_db
    """
    获取表格结构和示例数据
    返回:
    str: 获取表格结构和示例数据。
    """
    return get_excel_info_head(sheets_db)


def set_sheets_db(db):
    global sheets_db
    sheets_db = db


def clear_sheets_db():
    global sheets_db
    sheets_db.clear()


def get_sheets_db():
    global sheets_db
    return sheets_db


def set_global(key, value):
    globals()[key] = value


def get_global():
    return globals()
