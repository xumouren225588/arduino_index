import csv
import os
import serial.tools.list_ports
import esptool

def read_csv(file_path):
    partitions = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip().startswith('# Name:'):
                parts = line.split(',')
                partition = {
                    'name': parts[0].split(': ')[1],
                    'type': parts[1].split(': ')[1],
                    'subtype': parts[2].split(': ')[1],
                    'offset': int(parts[3].split(': ')[1], 16),
                    'size': int(parts[4].split(': ')[1], 16),
                    'flags': parts[5].split(': ')[1].strip()
                }
                partitions.append(partition)
    return partitions

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

def flash_files(partitions, files, port):
    for partition in partitions:
        for file in files:
            if file.endswith('.ino.bin') and partition['name'] == 'app0':
                esptool.main(['--chip', 'esp32', '--port', port, '--baud', '115200', 'write_flash', hex(partition['offset']), file])
            elif file.endswith('.ino.partitions.bin') and partition['name'] == 'nvs':
                esptool.main(['--chip', 'esp32', '--port', port, '--baud', '115200', 'write_flash', hex(partition['offset']), file])
            elif file.endswith('.ino.bootloader.bin') and partition['name'] == 'otadata':
                esptool.main(['--chip', 'esp32', '--port', port, '--baud', '115200', 'write_flash', hex(partition['offset']), file])

if __name__ == '__main__':
    csv_file_path = 'partitions.csv'
    directory = '.'  # 你可以指定文件所在的目录

    partitions = read_csv(csv_file_path)
    files = find_files(directory, ('.ino.bin', '.ino.partitions.bin', '.ino.bootloader.bin'))
    selected_port = list_ports_and_select()

    if selected_port:
        print(f"选择的串口: {selected_port}")
        try:
            flash_files(partitions, files, selected_port)
            print(f"烧录成功，使用串口: {selected_port}")
        except Exception as e:
            print(f"烧录失败，使用串口: {selected_port}，错误信息: {e}")
