# gitlab-backup使用说明

通过使用python-gitlab调用gitlab API遍历repositories对其进行备份。  

如果git repository在本地存在则进行git fetch，反之则进行git pull。

1. 安装依赖
> ```
> pip install -r requirements.txt
> 注意：
> - python版本应为2.7(python-gitlab不兼容python2.6)；建议将其加入到环境变量中
> - 根据需要有可能需要安装setuptools、pip
> ```

2. 修改自定义配置
> ```
> 修改settings.py中的配置（gitlab相关配置、是否允许邮件通知、smtp相关配置）
> 注意：
> - git url目前只支持http协议
> - gitlab的用户必须是管理员
> ```

3. 运行脚本
> ```
> python gitlab-backup.py
> ```

4. 建议
> ```
> 建议将备份任务放到crontab定时任务中
> - 01 02 * * * . $HOME/.bash_profile;/usr/bin/python /data/gitlab-backup/gitlab-backup.py>/var/log/gitlab-backup.log 2>&1
> - git环境变量应追加到.bash_profile文件中的PATH中
> ```