import hid
from threading import Thread
from time import sleep
from device_list_reader import DeviceListReader


class HIDListener:
    def __init__(self, vid, pid, target_interface=2):
        self.v_id = vid
        self.p_id = pid
        self.target_interface = target_interface
        self.data = None
        self.device = DeviceListReader('0x' + format(self.v_id, '04X'), '0x' + format(self.p_id, '04X'))

    def get_data(self):
        if self.data is None:
            return None
        return self.data[self.device.get_posBattery()]

    def start(self):
        thread = Thread(target=self._listen, daemon=True)
        thread.start()

    def _listen(self):
        try:
            h = hid.device()
            path = self._initialize()
            if path:
                h.open_path(path)
                h.set_nonblocking(True)
                while True:
                    data_temp = h.read(64)
                    if data_temp:
                        self.data = data_temp
                        sleep(10)

            else:
                print("cannot reach specific device")
        except IOError as ex:
            print(f"错误: {ex}")

    def _initialize(self):
        for device_dict in hid.enumerate(self.v_id, self.p_id):
            if device_dict['interface_number'] == self.target_interface and device_dict["usage_page"] == 10:
                return device_dict['path']
        return None
