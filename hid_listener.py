import hid
from threading import Thread
from time import sleep

class HIDListener:
    def __init__(self):
        self.v_id = 0x1D57
        self.p_id = 0xFA60
        self.target_interface = 2
        self.data = None
        self.running = True

    def get_data(self):
        return self.data

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
                while self.running:
                    data_temp = h.read(64)
                    if data_temp:
                        self.data = data_temp
                        sleep(5)
        except IOError as ex:
            print(f"错误: {ex}")

    def _initialize(self):
        for device_dict in hid.enumerate(self.v_id, self.p_id):
            if device_dict['interface_number'] == self.target_interface:
                return device_dict['path']
        return None
