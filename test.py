import os
import serial.tools.list_ports
import esptool

def find_files(directory, suffix):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(suffix):
                files.append(os.path.join(root, filename))
    return files

def get_available_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def list_ports_and_select():
    available_ports = get_available_ports()
    if not available_ports:
        print("没有找到可用的串口。")
        return None
    print("可用的串口列表：")
    for i, port in enumerate(available_ports):
        print(f"{i + 1}: {port}")
    while True:
        try:
            choice = int(input("请输入选择的串口编号: "))
            if 1 <= choice <= len(available_ports):
                return available_ports[choice - 1]
            else:
                print("无效的编号，请重新输入。")
        except ValueError:
            print("无效的输入，请输入一个数字。")

def flash_files(files, port):
    bootloader_file = next((file for file in files if file.endswith('.ino.bootloader.bin')), None)
    app_file = next((file for file in files if file.endswith('.ino.bin')), None)
    partitions_file = next((file for file in files if file.endswith('.ino.partitions.bin')), None)

    if bootloader_file:
        esptool.main(['--chip', 'esp32', '--port', port, '--baud', '115200', 'write_flash', '0x0000', bootloader_file])
    if partitions_file:
        esptool.main(['--chip', 'esp32', '--port', port, '--baud', '115200', 'write_flash', '0x8000', partitions_file])
    if app_file:
        esptool.main(['--chip', 'esp32', '--port', port, '--baud', '115200', 'write_flash', '0x10000', app_file])

if __name__ == '__main__':
    directory = '.'  # 你可以指定文件所在的目录

    files = find_files(directory, ('.ino.bin', '.ino.partitions.bin', '.ino.bootloader.bin'))
    selected_port = list_ports_and_select()

    if selected_port:
        print(f"选择的串口: {selected_port}")
        try:
            flash_files(files, selected_port)
            print(f"烧录成功，使用串口: {selected_port}")
        except Exception as e:
            print(f"烧录失败，使用串口: {selected_port}，错误信息: {e}")
