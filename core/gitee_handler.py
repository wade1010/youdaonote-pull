import requests
import logging


def create_repo(token, repo_name, username):
    url = "https://gitee.com/api/v5/user/repos"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"token {token}"
    }
    data = {
        "name": repo_name,
        "private": False,  # 空仓库不支持设置为公开,这里设置了也没用
        "description": "my note image-bed"
    }
    response = requests.post(url, json=data, headers=headers)
    upload_file_to_repo(token, repo_name, username)
    set_repo_public(token, repo_name, username)
    if response.status_code == 201:
        logging.info(f"Repository '{repo_name}' created successfully.")
        return True
    else:
        logging.warning(f"Failed to create repository: {response.json()}")
        return False


def upload_file_to_repo(token, repo_name, username, commit_message="initial commit"):
    url = f"https://gitee.com/api/v5/repos/{username}/{repo_name}/contents/README2.md"
    headers = {
        "Authorization": f"token {token}"
    }
    import base64
    encoded_content = base64.b64encode(
        "image-bed".encode('utf-8')).decode('utf-8')
    data = {
        "message": commit_message,
        "content": encoded_content
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        logging.info(f"File uploaded successfully.")
        return True
    else:
        logging.warning(f"Failed to upload file: {response.json()}")
        return False


def set_repo_public(token, repo_name, username):
    url = f"https://gitee.com/api/v5/repos/{username}/{repo_name}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"token {token}"
    }
    data = {
        "private": False,
        "name": repo_name
    }
    response = requests.patch(url, json=data, headers=headers)
    if response.status_code == 200:
        logging.info(f"Repository '{repo_name}' set to public successfully.")
        return True
    else:
        logging.warning(
            f"Failed to set repository to public: {response.json()}")
        return False
