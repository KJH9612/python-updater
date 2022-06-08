import boto3

import _version
import sys
import os
import errno
import subprocess

from pathlib import Path


class Updater:
    INSTALL_PATH = Path(__file__).resolve().parent.parent.parent
    DIR_FULL_PATH = Path(__file__).resolve().parent.parent
    THE_LINK = INSTALL_PATH / 'latest'
    CURRENT_VERSION = _version.__version__
    REGION = 'ap-northeast-2'
    s3_client = None
    def __init__(self):
        pass

    def updateCheck(self):
        print(self.CURRENT_VERSION)
        print(self.INSTALL_PATH)
        print(self.DIR_FULL_PATH)
        print(self.THE_LINK)

    def create_symlink_force(self, target, link_name):
        try:
            os.symlink(target, link_name)
        except OSError as e:
            if e.errno == errno.EEXIST:
                os.remove(link_name)
                os.symlink(target, link_name)
            else:
                raise e

    def is_windows_reparse_point(self, path: str) -> bool:
        """[Returns True if a path is a Windows Junction (reparse point)]
        Args:
            path (str)
        Returns:
            bool
        """
        try:
            return bool(os.readlink(path))
        except Exception:
            return False

    def create_symlink_cross_platform(self, target, link_name):
        """[Creates a reparse point on Windows or symbolik link on other OS]
        Args:
            target ([str])
            link_name ([str])
        """
        if sys.platform == 'win32':
            if self.is_windows_reparse_point(link_name):
                self.THE_LINK.unlink()
            subprocess.check_call('mklink /J "%s" "%s"' % (link_name, target), shell=True)
        else:
            self.create_symlink_force(target, link_name)

    def create_s3_client(self):
        session = boto3.Session(region_name=self.REGION, profile_name='dev')
        s3_client = session.client('s3')
        self.s3_client = s3_client
