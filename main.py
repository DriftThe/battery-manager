import pystray
from PIL import Image
from threading import Thread
from time import sleep
from hid_listener import HIDListener
from device_list_reader import DeviceEmulator, DeviceListReader
from device_finder import HIDEmulator
from common_function import *
import win32api
import win32event

mutex_name = 'device-battery-reader_app_mutex'
icon_normal = Image.open(resource_path('access/icon.png'))
icon_middle = Image.open(resource_path('access/icon-middlebattery.png'))
icon_low = Image.open(resource_path('access/icon-lowbattery.png'))
menu = pystray.Menu(
    pystray.MenuItem('退出', lambda instance: instance.stop())
)
icon = pystray.Icon(
    "app",
    icon_normal,
    "Default Title",
    menu
)
vid_from_json_set = {}
hid_from_pc_set = {}
supported_devices_vid_pid = []
supported_devices_string = []
hid_listening = []


def _app_init():
    global vid_from_json_set, hid_from_pc_set
    # 检查互斥
    try:
        _ = win32event.CreateMutex(None, False, mutex_name)
        if win32api.GetLastError() == 183:
            raise SystemExit("program is already running")
    finally:
        pass
    # 检查互斥结束
    # 读取json并存入到集合中
    vid_from_json_set = DeviceEmulator().get_devices_list()
    # 读取json并存入到集合中结束
    # 扫描电脑HID设备并与json_list进行比较
    hid_from_pc_set = HIDEmulator().get_hid_list()
    vid_pid_compare()
    print(f"支持的设备为:{supported_devices_string}")
    print(f"支持设备的vid与pid:{supported_devices_vid_pid}")
    # 扫描电脑HID设备并与json_list进行比较结束
    # 将支持的vid和pid列表传入监听器，监听器启动监听进程
    for i in supported_devices_vid_pid:
        v, p = i
        _device_to_listener(v, p)
    for i in hid_listening:
        i.start()
    main_thread = Thread(target=tray_thread, daemon=True)
    main_thread.start()
    # 将支持的vid和pid列表传入监听器，监听器启动监听进程结束
    if supported_devices_vid_pid:
        notify(f"supported devices found:{supported_devices_string}")
    else:
        notify(f"no supported device found,exiting")
        raise SystemExit("no supported device found")
    try:
        while main_thread.is_alive():
            sleep(0.1)
    except KeyboardInterrupt:
        pass


def vid_pid_compare():
    global vid_from_json_set, hid_from_pc_set, supported_devices_vid_pid, supported_devices_string
    supported_devices_vid_pid = []
    supported_devices_string = []
    for v, p in hid_from_pc_set:
        if v in vid_from_json_set:
            if p in DeviceListReader('0x' + format(v, '04X')).get_pids():
                supported_devices_vid_pid.append((v, p))
    if supported_devices_vid_pid is not None:
        for i in supported_devices_vid_pid:
            v, p = i
            supported_devices_string.append(
                DeviceListReader('0x' + format(v, '04X'), "0x" + format(p, '04X')).get_model())


def _device_to_listener(vid: int, pid: int):
    global hid_listening
    hid_listening.append(HIDListener(vid, pid))


def tray_thread():
    thread_update_title = Thread(target=update_info_thread, args=(icon,), daemon=True)
    thread_update_title.start()
    icon.run()


def update_info_thread(instance):
    isnotify = False
    device_count = 0
    battery_list = []
    title_string = ""
    notify_string = ""
    notify_sleep_count = 3600
    while True:
        for device in hid_listening:
            battery_list.append(device.get_data())
        for battery in battery_list:
            if battery is not None:
                title_string += supported_devices_string[device_count] + ': ' + str(battery) + '%'
            else:
                title_string += supported_devices_string[device_count] + ': ' + 'NAN' + '%'
            device_count += 1
            if device_count < len(supported_devices_vid_pid):
                title_string += '\n'
        device_count = 0
        instance.title = title_string
        for battery in battery_list:
            if battery is not None:
                if battery < 25:
                    instance.icon = icon_low
                    break
                if battery < 50:
                    instance.icon = icon_middle
                    break
                instance.icon = icon_normal
        for battery in battery_list:
            if battery is not None:
                if battery <= 25:
                    notify_string += supported_devices_string[device_count] + ': ' + str(battery) + '%'
                    isnotify = True
                    if notify_sleep_count < 3600:
                        notify_sleep_count += 1
        if isnotify and notify_sleep_count == 3600:
            notify(notify_string)
            isnotify = False
            notify_sleep_count = 0
        battery_list.clear()
        title_string = ""
        notify_string = ""
        sleep(1)


_app_init()
