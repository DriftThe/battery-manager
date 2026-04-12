import hid


# 按VID排序


class HIDEmulator:
    def __init__(self):
        self.devices = hid.enumerate()
        self.seen = set()
        self.sorted_devices = sorted(self.devices, key=lambda x: (x['vendor_id'], x['product_id']))
        self.hid_return = set()
        for device in self.sorted_devices:
            vid = device['vendor_id']
            pid = device['product_id']
            key = (vid, pid)
            if key not in self.seen:
                self.seen.add(key)
                # name = device['product_string']
                # print(f"VID: 0x{vid:04X}, PID: 0x{pid:04X}, 名称: {name}")
        for i, e in enumerate(self.seen):
            self.hid_return.add(e)

    def get_hid_list(self):
        return self.hid_return


D = HIDEmulator()
