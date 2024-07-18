import os
import sys
import re


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