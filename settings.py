# -*- coding:utf-8 -*-

# tips:the user of gitlab must be an administrator
GIT_SETTINGS = {
    'gitlab_url': 'http://git.example.com/',
    'private_token': 'private_token',
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