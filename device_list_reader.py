import json
from common_function import *


class DeviceListReader:
    def __init__(self, vid: str, pid: str = None):
        self.vid = vid
        self.pid = pid
        self.pids_return = set()
        with open(resource_path('./access/devices.json'), "r") as f:
            self.devices = json.load(f)
        if (not self.devices.get(self.vid, {}).get(self.pid)) and pid is not None:
            raise ValueError(f"Cannot find device in device_list: VID={vid}, PID={pid}")

    def get_vendor(self):
        return self.devices[self.vid][self.pid]["vendor"]

    def get_model(self):
        return self.devices[self.vid][self.pid]["model"]

    def get_isCommand(self):
        return bool(self.devices[self.vid][self.pid]["isCommand"])

    def get_Command(self):
        lst1d = self.devices[self.vid][self.pid]["Command"].split(";")
        lst2d = [[int(num) for num in row.split(',')] for row in lst1d]
        return lst2d

    def get_numCommand(self):
        return len(self.get_Command())

    def get_isSign(self):
        return bool(self.devices[self.vid][self.pid]["isSign"])

    def get_posSign(self):
        return int(self.devices[self.vid][self.pid]["posSign"])

    def get_Sign(self):
        return int(self.devices[self.vid][self.pid]["Sign"])

    def get_posBattery(self):
        return int(self.devices[self.vid][self.pid]["posBattery"])

    def get_pids(self):
        self.pids_return.clear()
        if not self.devices.get(self.vid):
            raise ValueError(f"Cannot find device in device_list: VID={self.vid}")
        else:
            for i in self.devices[self.vid]:
                self.pids_return.add(int(i, 16))
            return self.pids_return


class DeviceEmulator:
    def __init__(self):
        self.devices_vid_list = set()
        with open(resource_path('./access/devices.json'), "r") as f:
            self.devices_from_json = json.load(f)
            for vid in self.devices_from_json:
                self.devices_vid_list.add(int(vid, 16))

    def get_devices_list(self):
        return self.devices_vid_list


if __name__ == "__main__":
    D = DeviceListReader("0x1D57").get_pids()
