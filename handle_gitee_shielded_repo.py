import os
import shutil
import math
import re

"""
处理超大容量的 gitee 仓库，我之前所有笔记的图片都放到了同一个仓库，导致该仓库被 gitee 屏蔽，参考 https://blog.csdn.net/wade1010/article/details/140508131
"""


def split_files_and_generate_links(src_dir, dest_dir_base, num_splits, base_url, output_file):
    # 获取所有文件列表
    files = os.listdir(src_dir)
    total_files = len(files)
    files_per_split = math.ceil(total_files / num_splits)

    if not os.path.exists(dest_dir_base):
        os.makedirs(dest_dir_base)

    # 创建新目录
    for i in range(num_splits):
        new_dir = os.path.join(dest_dir_base, f'images{i}')
        if not os.path.exists(new_dir):
            os.makedirs(os.path.join(new_dir, 'img'))

    # 分配文件并生成链接
    current_split = 0
    current_count = 0
    with open(output_file, 'w') as f:
        for file in files:
            # 计算当前文件应分配到哪个目录
            if current_count >= files_per_split:
                current_split += 1
                current_count = 0

            src_file = os.path.join(src_dir, file)
            dest_dir = os.path.join(
                dest_dir_base, f'images{current_split}', 'img')
            dest_file = os.path.join(dest_dir, file)

            # 移动文件到新目录
            shutil.move(src_file, dest_file)

            # 生成新的链接
            new_url = f'{base_url}{current_split}/raw/master/img/{file}'
            f.write(new_url + '\n')

            current_count += 1


def generate_mapping(url_file):
    """
    解析url.txt文件生成文件名到URL的映射。
    """
    mapping = {}
    with open(url_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                # 解析出文件名
                filename = line.split('/')[-1]
                mapping[filename] = line
    return mapping


def update_markdown_files(md_directory, mapping, old_base_url):
    """
    循环指定目录，找到所有.md文件，并进行URL替换。
    """
    for root, _, files in os.walk(md_directory):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 查找需要替换的URL
                pattern = re.compile(
                    re.escape(old_base_url) + r'/img/(\S+?\.jpg)')
                matches = pattern.findall(content)
                for match in matches:
                    filename = match
                    if filename in mapping:
                        old_url = f'{old_base_url}/img/{filename}'
                        new_url = mapping[filename]
                        content = content.replace(old_url, new_url)

                # 写回文件
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)


if __name__ == "__main__":
    # -------开始  分割并生成url  -------
    # 容量超过限制的仓库下载到本地的目录+前缀目录(这里是img)
    src_directory = r"D:/工作空间/images/img"
    # 分割后的仓库存放目录
    dest_directory_base = r"D:/工作空间"
    # 总容量 MB //450 MB 的值就是 splits，确保每个仓库不足500 MB
    splits = 6
    # 你的仓库地址，xxx 是你的 username ，images 是分割手基础的仓库名，会拼接位 images0、images1等
    base_url = "https://gitee.com/xxx/images"
    # 所有 gitee 图片的 url
    url_file_path = r"D:/工作空间/url.txt"

    split_files_and_generate_links(
        src_directory, dest_directory_base, splits, base_url, url_file_path)
    # -------结束  分割并生成url  -------

    # 然后把 上面分割后的仓库都传到你自己的 gitee 仓库名要跟目录一致，上传完成后，再执行下面代码

    answer = input(f"是否已经把分割后的目录上传到 gitee ?(yes/on)")

    if answer.lower() == "yes":
        # -------开始  更改 markdown 里面的 URL 链接为分割后的链接  -------
        md_directory_path = r"D:/工作空间/images"
        # 容量超过限制的仓库的地址，截止到 master 部分 ,xxx 是你的 username， images0 是你超过容量的仓库名
        old_base_url = "https://gitee.com/xxx/images0/raw/master"

        url_mapping = generate_mapping(url_file_path)
        update_markdown_files(md_directory_path, url_mapping, old_base_url)
