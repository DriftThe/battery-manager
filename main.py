import pystray
from PIL import Image
from threading import Thread
from time import sleep
from hid_listener import HIDListener
import sys
import os


def resource_path(relative_path):
    """获取打包后资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        # 如果是打包后的环境
        base_path = sys._MEIPASS
    else:
        # 开发环境，直接使用当前路径
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


hid_class = HIDListener()
hid_class.start()


def tray_thread():
    image = Image.open(resource_path('./icon.png'))
    menu = pystray.Menu(
        pystray.MenuItem('退出', lambda icon: icon.stop())
    )

    icon = pystray.Icon(
        "app",
        image,
        "Default Title",
        menu
    )
    thread_update_title = Thread(target=update_thread, args=(icon,), daemon=True)
    thread_update_title.start()
    icon.run()


def listen_hid_thread():
    hid_class.start()


def update_thread(instance):
    flag = 0
    while True:
        data = hid_class.get_data()
        if data:
            instance.title = f'Mouse Battery: {data[4]}'
            flag = 1
            sleep(5)
        elif flag == 0:
            instance.title = 'Mouse Battery: NaN'


thread_main = Thread(target=tray_thread, daemon=True)
thread_main.start()


try:
    while thread_main.is_alive():
        sleep(0.1)
    print("exit")
except KeyboardInterrupt:
    pass
