import sqlite3
import os

def get_corsor(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return cursor

def get_emotion_data(cursor):
    sql_str = """
                SELECT *
                FROM (
                SELECT EmotionDes1.ProductId, EmotionDes1.Des, EmotionItem.Data
                FROM EmotionDes1, EmotionItem
                WHERE EmotionDes1.MD5 = EmotionItem.MD5)
                AS tab1,(
                SELECT ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS RowNum,
                EmotionPackageItem.Name
                FROM EmotionPackageItem) AS tab2
                WHERE tab1.ProductId = tab2.RowNum
            """
    cursor.execute(sql_str)
    result = cursor.fetchall()
    return result

def save_to_sys(result, save_path):
    for item in result:
        Des = item[1][6:].decode("utf-8")
        Data = item[2]
        Package = item[4]
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        Package_path = os.path.join(save_path, Package)
        if not os.path.exists(Package_path):
            os.makedirs(Package_path)
        with open(os.path.join(Package_path, Des + ".gif"), "wb+") as f:
            f.write(Data)

def parse():
    db_path = "./data/Emotion.db"
    cursor = get_corsor(db_path)
    result = get_emotion_data(cursor)
    save_path = "./Emotion"
    save_to_sys(result, save_path)