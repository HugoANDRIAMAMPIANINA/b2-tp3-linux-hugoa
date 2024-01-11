from argparse import ArgumentParser
from psutil import virtual_memory, disk_usage, cpu_percent
import socket
from contextlib import closing
from json import load, dump
from os.path import isfile, exists
from os import makedirs
from uuid import uuid1
from datetime import datetime


def file_exists(file_path):
    if exists(file_path) and isfile(file_path):
        return True
    return False

def create_file(file_directory, file_name, json_data):
    if not exists(file_directory):
        makedirs(file_directory)
    
    with open(f"{file_directory}{file_name}", "w") as conf_file:
        dump(json_data, conf_file)

def get_ram_informations():
    ram = virtual_memory()
    
    total_ram = ram.total
    available_ram = ram.available
    used_ram = ram.used
    free_ram = ram.free
    percent_used = ram.percent
    
    return total_ram, available_ram, used_ram, free_ram, percent_used

def get_disk_usage():
    # try catch maybe ?
    disk = disk_usage('/')
    
    total_disk = disk.total / 1024 / 1024 / 1024
    free_disk = disk.free / 1024 / 1024 / 1024
    used_disk = disk.used / 1024 / 1024 / 1024
    percent_used = disk.percent
    
    return total_disk, free_disk, used_disk, percent_used

def get_cpu_usage():
    return cpu_percent()

def is_port_open(port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        socket.setdefaulttimeout(2.0)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            sock.close()
            return True
        else:
            sock.close()
            return False

def check_tcp_ports():
    with open('/etc/monit/monit.conf') as conf_file:
        config = load(conf_file)
    
    ports = config["tcp_ports"]
    print(ports)
    
    ports_checking_report = {}
    for port in ports:
        is_open = is_port_open(port)
        ports_checking_report[str(port)] = is_open
        
    return ports_checking_report

def get_id():
    return uuid1().int

def get_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
def create_report_file_json():
    total_ram, available_ram, used_ram, free_ram, percent_used_ram = get_ram_informations()
    total_disk, free_disk, used_disk, percent_used_disk = get_disk_usage()
    percent_used_cpu = get_cpu_usage()
    tcp_ports_info = check_tcp_ports()
    report_json = {
        "id": get_id(),
        "date": get_datetime(),
        "ram": {
            "total_ram": total_ram,
            "available_ram": available_ram,
            "used_ram": used_ram,
            "free_ram": free_ram,
            "percent_used": percent_used_ram
        },
        "disk": {
            "total_disk": total_disk,
            "free_disk": free_disk,
            "used_disk": used_disk,
            "percent_used": percent_used_disk
        },
        "cpu": {
            "percent_used": percent_used_cpu
        }
    }
    if tcp_ports_info != {}:
        report_json["tcp_ports": tcp_ports_info]
        
    return report_json

def check_system():
    report_file_name = f"monit_{datetime.now().strftime("%Y%m%d%H%M%S")}"
    print(report_file_name)
    create_file("/var/monit",report_file_name, create_report_file_json())
    
def main():
    parser = ArgumentParser()
    g = parser.add_mutually_exclusive_group()
    
    g.add_argument("-c", "--check", action="store_true")
    g.add_argument("-l", "--list", action="store_true")
    g.add_argument("--get-last", action="store_true")
    g.add_argument("--get-avg", action="store")
    
    args = parser.parse_args()
    print(args)
    
    if not file_exists('/etc/monit/monit.conf'):
        create_file("/etc/monit/", "monit.conf", { "tcp_ports": [] })
        
    check_system()


if __name__ == "__main__":
    main()