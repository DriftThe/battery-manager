import os
import sys
from win32com.client import Dispatch
import pythoncom


class StartupManager:
    def __init__(self):
        self.shortcut_flag = False
        self.appdata = os.getenv('APPDATA', None)
        if self.appdata is not None:
            self.startup_folder = os.path.join(self.appdata, r'Microsoft\Windows\Start Menu\Programs\Startup')
        else:
            raise ValueError("Cannot find startup folder")
        self.app_name = os.path.splitext(os.path.basename(sys.executable))[0]
        self.shortcut_path = os.path.join(self.startup_folder, f"{self.app_name}.lnk")

    def _check_shortcut(self):
        if not os.path.exists(self.shortcut_path):
            self.shortcut_flag = False
            return False
        else:
            self.shortcut_flag = True
            return True

    def toggle_launch_when_up_shortcut(self):
        self._check_shortcut()
        if not self.shortcut_flag:
            """如果没有创建过shortcut，就创建"""
            try:
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(self.shortcut_path)
                shortcut.TargetPath = sys.executable
                shortcut.WorkingDirectory = os.path.dirname(sys.executable)
                shortcut.save()
                self.shortcut_flag = True
            finally:
                pythoncom.CoUninitialize()
        else:
            """如果已经创建过shortcut，则删除"""
            os.remove(self.shortcut_path)
            self.shortcut_flag = False

    def get_shortcut_flag(self):
        self._check_shortcut()
        return self.shortcut_flag
