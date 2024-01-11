from argparse import ArgumentParser
from psutil import virtual_memory, disk_usage, cpu_percent
import socket
from json import load, dump
from os.path import isfile, exists
from os import makedirs


def conf_file_exists():
    conf_file_path = '/etc/monit/monit.conf'
    if exists(conf_file_path) and isfile(conf_file_path):
        return True
    return False

def create_config_file():
    directory = "/etc/monit"
    
    if not exists(directory):
        makedirs(directory)
    
    conf_json = { "tcp_ports": [] }
    with open("/etc/monit/monit.conf", "w") as conf_file:
        dump(conf_json, conf_file)

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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    

def check_system():
    # total_ram, available_ram, used_ram, free_ram, percent_used_ram = get_ram_informations()
    # total_disk, free_disk, used_disk, percent_used_disk = get_disk_usage()
    # percent_used_cpu = get_cpu_usage()
    print(check_tcp_ports())
    
def main():
    parser = ArgumentParser()
    g = parser.add_mutually_exclusive_group()
    
    g.add_argument("-c", "--check", action="store_true")
    g.add_argument("-l", "--list", action="store_true")
    g.add_argument("--get-last", action="store_true")
    g.add_argument("--get-avg", action="store")
    
    args = parser.parse_args()
    print(args)
    
    if not conf_file_exists():
        create_config_file()
        
    check_system()


if __name__ == "__main__":
    main()