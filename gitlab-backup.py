# -*- coding: utf-8 -*-
import os
import logging

import gitlab

from settings import GIT_SETTINGS
from settings import MAIL_SETTINGS
from settings import LOG_SETTINGS
from settings import MAIL_NOTIFY_ENABLE

from custome_logging import BufferingSMTPHandler
from custome_logging import ConsoleHandler


def get_gitlab_instance():
    gitlab_url = GIT_SETTINGS.get('gitlab_url')
    private_token = GIT_SETTINGS.get('private_token')
    gitlab_server = gitlab.Gitlab(gitlab_url, private_token=private_token)
    gitlab_server.auth()
    return gitlab_server


def record_log_with_level(logger, output):
    if output.strip().startswith("fatal") or output.strip().startswith("error"):
        logger.error(output.strip())
    else:
        logger.info(output.strip())


def backup_git_repo(logger):
    # backup git repo by paging
    page = 1
    while True:
        backup_git_by_page(page, logger)
        page += 1


def backup_git_by_page(page, logger):
    git = get_gitlab_instance()
    projects = git.projects.all(page=page, per_page=100)
    git_data_path = GIT_SETTINGS.get('git_data_path')
    if 0 == len(projects):
        logger.info("All projects backup completed !")
        exit(0)
    else:
        logger.info("There are %s projects on page %s." % (len(projects), page))
        try:
            for project in projects:
                git_repo_path = os.path.join(git_data_path, project.path_with_namespace + ".git")
                logger.debug("begin to backup git repo %s !" % project.path_with_namespace)

                # if the project has been cloned,then exec git fetch command,else exec git clone command.
                if os.path.exists(git_repo_path):
                    os.chdir(git_repo_path)
                    for output in os.popen("git fetch 2>&1"):
                        record_log_with_level(logger, output)
                else:
                    for output in os.popen("git clone --mirror %s %s 2>&1" % (project.http_url_to_repo, git_repo_path)):
                        record_log_with_level(logger, output)
        except:
            logger.exception('Got exception on logger handler:')
            raise
        logger.info("The projects of page %s backup completed !" % page)


def main():
    # get log level from settings
    log_level = LOG_SETTINGS.get('level')

    # setup logger and handler
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    logger.addHandler(ConsoleHandler())
    if MAIL_NOTIFY_ENABLE:
        mailhost = MAIL_SETTINGS.get('mailhost')
        mail_username = MAIL_SETTINGS.get('username')
        mail_password = MAIL_SETTINGS.get('password')
        fromaddr = MAIL_SETTINGS.get('fromaddr')
        toaddrs = MAIL_SETTINGS.get('toaddrs')
        subject = MAIL_SETTINGS.get('subject')
        logger.addHandler(BufferingSMTPHandler(mailhost, fromaddr, toaddrs, subject, mail_username, mail_password, 10000))

    # backup git repo
    backup_git_repo(logger)

if __name__ == "__main__":
    main()