# -*- coding:utf-8 -*-

# tips:the user of gitlab must be an administrator
GIT_SETTINGS = {
    'gitlab_url': 'https://gitlab.example.com',
    'private_token': '9koXpg98eAheJpvBs5tK',
    'git_data_path': '/data/git-data/repositories'
}

MAIL_NOTIFY_ENABLE = True

MAIL_SETTINGS = {
    'mailhost': 'smtp.xxx.com',
    'username': 'xxx@xxx.com',
    'password': 'xxx',
    'fromaddr': 'xxx@xxx.com',
    'toaddrs': ['xxx@xxx.com', 'xxx@xxx.com'],
    'subject': 'Gitlab Backup E-mail Notification'
}

LOG_SETTINGS = {
    'level': 'INFO',
}