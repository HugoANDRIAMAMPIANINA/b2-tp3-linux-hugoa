import socket
from contextlib import closing
from json import load
from psutil import virtual_memory, disk_usage, cpu_percent


def get_ram_informations():
    ram = virtual_memory()

    total_ram = round(ram.total / 1000000000, 2)
    available_ram = round(ram.available / 1000000000, 2)
    used_ram = round(ram.used / 1000000000, 2)
    free_ram = round(ram.free / 1000000000, 2)
    percent_used = ram.percent

    return total_ram, available_ram, used_ram, free_ram, percent_used


def get_disk_usage():
    disk = disk_usage('/')

    total_disk = round(disk.total / 1024 / 1024 / 1024, 2)
    free_disk = round(disk.free / 1024 / 1024 / 1024, 2)
    used_disk = round(disk.used / 1024 / 1024 / 1024, 2)
    percent_used = disk.percent

    return total_disk, free_disk, used_disk, percent_used


def get_cpu_usage():
    return cpu_percent()


def is_port_open(port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        socket.setdefaulttimeout(2.0)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        if result == 0:
            return True
        return False


def check_tcp_ports():
    with open('/etc/monit/monit.conf', 'r', encoding='utf-8') as conf_file:
        config = load(conf_file)

    ports = config["tcp_ports"]

    ports_checking_report = {}
    for port in ports:
        is_open = is_port_open(port)
        ports_checking_report[str(port)] = is_open

    return ports_checking_report
