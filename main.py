import pystray
from PIL import Image
from threading import Thread
from time import sleep
from hid_listener import HIDListener
import sys
import os
from winotify import Notification
import win32api
import win32event

mutex_name = 'device-battery-reader_app_mutex'
try:
    mutex = win32event.CreateMutex(None, False, mutex_name)
    if win32api.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        print("程序已在运行中")
        raise SystemExit()
finally:
    pass


def resource_path(relative_path):
    """获取打包后资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def notify(string: str):
    toaster = Notification(
        "Mouse Battery",
        string,
        "",
    )
    toaster.show()


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
    notify("Mouse Battery is running now")
    icon.run()


def listen_hid_thread():
    hid_class.start()


def update_thread(instance):
    flag = 0
    count = 360
    while True:
        data = hid_class.get_data()
        if data:
            instance.title = f'Mouse Battery: {data[4]}'
            flag = 1
            count = count + 1
            sleep(10)
            if data[4] <= 25 and count >= 720:
                count = 0
                notify(f"Mouse in low battery: {data[4]}%")
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
