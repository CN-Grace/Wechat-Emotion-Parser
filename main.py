from util.get_wx_info import read_info, get_wechat_db
from util.decryption import decrypt
from util.data_parse import parse
import os, json

def main():
    try:
      VERSION_LIST_PATH = os.path.join(os.path.dirname(__file__), "version_list.json")
      with open(VERSION_LIST_PATH, "r", encoding="utf-8") as f:
          VERSION_LIST = json.load(f)
    except:
        VERSION_LIST = {}
        VERSION_LIST_PATH = None
    info = read_info(VERSION_LIST, is_logging=True)
    path = get_wechat_db("Emotion", is_logging=True)
    data_path = "./data"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    result = decrypt(info[0]['key'], path[info[0]['filePath']]['Emotion'][0], "./data/Emotion.db")
    if result[0]:
        parse()


if __name__ == "__main__":
    main()