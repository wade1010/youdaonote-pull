import os
import sys
import re
import json


def get_script_directory():
    """获取脚本所在的目录"""

    if getattr(sys, "frozen", False):
        # 如果是打包后的可执行文件
        return os.path.dirname(sys.executable)
    else:
        # 如果是普通脚本
        return "."


def increment_string(s):
    match = re.search(r"(\D+)(\d+)", s)  # 匹配字母后面的数字部分
    if match:
        prefix = match.group(1)
        suffix = match.group(2)
        next_num = int(suffix) + 1
        next_string = f"{prefix}{next_num}"
        return next_string
    else:
        return None


def update_config(field, value, config_file):
    # 检查配置文件是否存在
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"{config_file} 文件不存在")

    # 读取配置文件内容
    with open(config_file, 'r', encoding='utf-8') as file:
        config_data = json.load(file)

    config_data[field] = value

    # 写回配置文件
    with open(config_file, 'w', encoding='utf-8') as file:
        json.dump(config_data, file, ensure_ascii=False, indent=4)
