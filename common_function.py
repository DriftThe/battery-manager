from winotify import audio, Notification
import sys
import os


def notify(string: str):
    """创建系统通知"""
    toaster = Notification(
        "Battery Manager",
        string,
        "",
        duration='short'
    )
    toaster.set_audio(audio.Default, loop=False)
    toaster.show()


def resource_path(relative_path):
    """获取打包后资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
