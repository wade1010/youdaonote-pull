import requests
import logging

def create_repo(token, repo_name):
    url = "https://gitee.com/api/v5/user/repos"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"token {token}"
    }
    data = {
        "name": repo_name,
        "private": False, # 图床默认是公开
        "description": "my note image-bed"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        logging.info(f"Repository '{repo_name}' created successfully.")
        return True
    else:
        logging.warning(f"Failed to create repository: {response.json()}")
        return False