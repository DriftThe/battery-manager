# HID设备电池管理 / HID Battery Manager

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Windows](https://img.shields.io/badge/Platform-Windows-0078D7.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

一个用于读取HID设备电池电量的Windows系统托盘应用程序 / A Windows system tray application for reading HID device battery
levels

[中文](#中文文档) | [English](#english-documentation)

</div>

---

## 中文文档

### 简介

设备电池读取器是一个Windows系统托盘应用程序，用于实时监控HID设备的电池电量，并在低电量时发送系统通知。

### 功能特性

- 📊 实时监控HID无线设备电池电量
- 🔔 低电量系统通知提醒（≤25%）
- 🖥️ 系统托盘图标显示电池状态
- 🎨 根据电量自动切换托盘图标颜色
- 📱 支持多设备同时监控

### 支持的设备型号

| 厂商     | 型号   | VID    | PID    | 状态    |
|--------|------|--------|--------|-------|
| Inphic | IN-6 | 0x1D57 | 0xFA60 | ✅ 已支持 |

### 安装与使用

#### 环境要求

- Windows 10/11 操作系统
- Python 3.8+
- 管理员权限（首次运行可能需要）

#### 安装步骤

1. 克隆或下载项目到本地
2. 安装依赖库：
   ```bash
   pip install -r requirements.txt
   ```
3. 打包为可执行文件（可选）：
   ```bash
   pyinstaller --name "Battery Manager" --noconsole --onefile --icon=./access/icon.png --add-data "./access;./access" main.py
   ```
4. 运行程序：
    - Python直接运行：`python main.py`
    - 或运行打包后的程序：`./dist/Battery Manager.exe`

#### 程序界面

程序启动后会在系统托盘显示电池图标：

- 白色图标：电量正常（≥50%）
- 黄色图标：电量中等（25%-50%）
- 红色图标：电量低（＜25%）

右键点击托盘图标可选择"退出"程序。

### 项目结构

```
device-battery-reader/
├── main.py                    # 主程序入口
├── requirements.txt           # Python依赖库
├── common_function.py         # 通用函数（通知、资源路径）
├── device_finder.py           # HID设备查找器
├── device_list_reader.py      # 设备列表读取器
├── hid_listener.py            # HID监听器
├── access/                    # 资源文件目录
│   ├── devices.json          # 设备配置文件
│   ├── icon.png              # 主图标
│   ├── icon-middlebattery.png # 中等电量图标
│   └── icon-lowbattery.png   # 低电量图标
└── README.md                 # 说明文档
```

### 开发与扩展

#### 添加新设备支持

要添加新的设备支持，请编辑 `access/devices.json` 文件：

```json
{
  "0xVID": {
    "0xPID": {
      "vendor": "厂商名称",
      "model": "设备型号",
      "usage_page": "电池信息对应的使用页",
      "wire_pid": "有线连接时的pid",
      "target_interface": "2",
      "isCommand": "是否需要先发送命令报文",
      "Command": "命令报文内容",
      "isSign": "接收报文是否以标头区分",
      "posSign": "标头位置",
      "Sign": "标头内容",
      "posBattery": "电池数据位置"
    }
  }
}
```

#### 构建可执行文件

使用PyInstaller打包时，确保包含资源文件：

```bash
pyinstaller --name "Battery Manager" --noconsole --onefile --icon=./access/icon.png --add-data "./access;./access" main.py
```

### 故障排除

#### 常见问题

- **Q: 程序启动后立即退出？**  
  A: 可能是没有检测到支持的设备，或者程序已在运行（单实例限制）。

- **Q: 电池电量显示为NAN？**  
  A: 设备连接异常或电池数据位置配置不正确。

- **Q: 打包后图标不显示？**  
  A: 确保使用 `--add-data` 参数正确包含access目录。

#### 调试模式

如需查看详细日志，可修改代码移除 `--noconsole` 参数重新打包。

### 许可证

本项目采用 MIT 许可证。

### 贡献

欢迎提交Issue和Pull Request来改进本项目，特别是添加对新设备的支持。

---

## English Documentation

### Introduction

Device Battery Reader is a Windows system tray application for real-time monitoring of HID device battery levels and
sending system notifications when battery is low.

### Features

- 📊 Real-time HID wireless device battery monitoring
- 🔔 Low battery system notifications (≤25%)
- 🖥️ System tray icon displaying battery status
- 🎨 Automatic tray icon color switching based on battery level
- 📱 Support for multiple simultaneous device monitoring

### Supported Device Models

| Vendor | Model | VID    | PID    | Status      |
|--------|-------|--------|--------|-------------|
| Inphic | IN-6  | 0x1D57 | 0xFA60 | ✅ Supported |

### Installation & Usage

#### Requirements

- Windows 10/11 operating system
- Python 3.8+
- Administrator privileges (may be required for first run)

#### Installation Steps

1. Clone or download the project locally
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Package as executable (optional):
   ```bash
   pyinstaller --name "Battery Manager" --noconsole --onefile --icon=./access/icon.png --add-data "./access;./access" main.py
   ```
4. Run the program:
    - Direct Python execution: `python main.py`
    - Or run the packaged executable: `./dist/Battery Manager.exe`

#### Program Interface

After startup, the program displays a battery icon in the system tray:

- White icon: Normal battery (≥50%)
- Yellow icon: Medium battery (25%-50%)
- Red icon: Low battery (＜25%)

Right-click the tray icon to select "Exit" and quit the program.

### Project Structure

```
device-battery-reader/
├── main.py                    # Main program entry
├── requirements.txt           # Python dependencies
├── common_function.py         # Common functions (notifications, resource paths)
├── device_finder.py           # HID device finder
├── device_list_reader.py      # Device list reader
├── hid_listener.py            # HID listener
├── access/                    # Resource files directory
│   ├── devices.json          # Device configuration file
│   ├── icon.png              # Main icon
│   ├── icon-middlebattery.png # Medium battery icon
│   └── icon-lowbattery.png   # Low battery icon
└── README.md                 # Documentation
```

### Development & Extension

#### Adding New Device Support

To add support for new devices, edit the `access/devices.json` file:

```json
{
  "0xVID": {
    "0xPID": {
      "vendor": "Vendor Name",
      "model": "Device Model",
      "usage_page": "Usage page corresponding to battery information",
      "wire_pid": "PID when wired connection",
      "target_interface": "2",
      "isCommand": "Whether command packet needs to be sent first",
      "Command": "Command packet content",
      "isSign": "Whether received packet is distinguished by header",
      "posSign": "Header position",
      "Sign": "Header content",
      "posBattery": "Battery data position"
    }
  }
}
```

#### Building Executable

When packaging with PyInstaller, ensure resource files are included:

```bash
pyinstaller --name "Battery Manager" --noconsole --onefile --icon=./access/icon.png --add-data "./access;./access" main.py
```

### Troubleshooting

#### Common Issues

- **Q: Program exits immediately after startup?**  
  A: May be due to no supported devices detected, or program already running (single instance restriction).

- **Q: Battery level shows as NAN?**  
  A: Device connection issue or incorrect battery data position configuration.

- **Q: Icons not displaying after packaging?**  
  A: Ensure the `--add-data` parameter correctly includes the access directory.

#### Debug Mode

To view detailed logs, modify the code to remove the `--noconsole` parameter and repackage.

### License

This project is licensed under the MIT License.

### Contributing

Issues and Pull Requests are welcome to improve this project, especially for adding support for new devices.