from argparse import ArgumentParser
from psutil import virtual_memory, disk_usage, cpu_percent
import socket
from contextlib import closing
from json import load, dump
from os.path import isfile, exists
from os import makedirs, listdir
from uuid import uuid1
from datetime import datetime, timedelta
from sys import exit


def argument_management(parser):
    g = parser.add_mutually_exclusive_group()
    
    g.add_argument("-c", "--check", action="store_true", help="inspect RAM, CPU and Disk usage, check if TCP ports specified in config file (/etc/monit/monit.conf) are open and used, output the results and store these in a file located in /var/monit/")
    g.add_argument("-l", "--list", action="store_true", help="output all the check files name and path")
    g.add_argument("--get-last", action="store_true", help="output the last check file results")
    g.add_argument("--get-avg", action="store", type=int, help="output average check values since the last X hours, X is the integer value given in argument")
    
    return parser.parse_args()


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
    
    total_ram = round(ram.total / 1000000000, 2)
    available_ram = round(ram.available / 1000000000, 2)
    used_ram = round(ram.used / 1000000000, 2)
    free_ram = round(ram.free / 1000000000, 2)
    percent_used = ram.percent
    
    return total_ram, available_ram, used_ram, free_ram, percent_used


def get_disk_usage():
    # try catch maybe ?
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
    
    ports_checking_report = {}
    for port in ports:
        is_open = is_port_open(port)
        ports_checking_report[str(port)] = is_open
        
    return ports_checking_report

    
def create_report_file_json(check_id, check_date, ram_usage, disk_usage, cpu_usage, tcp_ports_info):
    total_ram, available_ram, used_ram, free_ram, percent_used_ram = ram_usage
    total_disk, free_disk, used_disk, percent_used_disk = disk_usage
    percent_used_cpu = cpu_usage 
    report_json = {"id":check_id,"date":check_date,"ram":{"total_ram":total_ram,"available_ram":available_ram,"used_ram":used_ram,"free_ram":free_ram,"percent_used":percent_used_ram},"disk":{"total_disk":total_disk,"free_disk":free_disk,"used_disk":used_disk,"percent_used":percent_used_disk},"cpu":{"percent_used":percent_used_cpu}}
    if tcp_ports_info != {}:
        report_json["tcp_ports"] = tcp_ports_info
        
    return report_json


def system_check():
    ram_usage = get_ram_informations()
    disk_usage = get_disk_usage()
    cpu_usage = get_cpu_usage()
    tcp_ports_info = check_tcp_ports()
    check_id, check_date, = uuid1().hex, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_file_name = f"monit_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    json_report_file = create_report_file_json(check_id, check_date, ram_usage, disk_usage, cpu_usage, tcp_ports_info)
    
    system_check_output(check_id, check_date, ram_usage, disk_usage, cpu_usage, tcp_ports_info)
    create_file("/var/monit/",report_file_name, json_report_file)
    
    
def system_check_output(check_id, check_date, ram_usage, disk_usage, cpu_usage, tcp_ports_info):
    total_ram, available_ram, used_ram, free_ram, percent_used_ram = ram_usage
    total_disk, free_disk, used_disk, percent_used_disk = disk_usage
    percent_used_cpu = cpu_usage 
    check_output = f"""
CHECK - {check_id}\n
Date: {check_date}\n
RAM: 
    Total RAM: {total_ram} GB
    Available RAM: {available_ram} GB
    Used RAM: {used_ram} GB
    Free RAM: {free_ram} GB
    Precent Used: {percent_used_ram}%\n 
Disk: 
    Total Disk: {total_disk} GB
    Free Disk: {free_disk} GB
    Used Disk: {used_disk} GB
    Percent Used: {percent_used_disk}%\n
CPU:
    Percent Used: {percent_used_cpu}%\n\n"""
    if tcp_ports_info != {}:
        ports_output = ""
        for port, status in tcp_ports_info.items():
            ports_output += f"    {port}: {status}\n"
        check_output += f"TCP PORTS:\n{ports_output}"
    
    print(check_output)
    
    
def read_json_file(file_path):
    json_data = load(file_path)
    check_id, check_date, ram_usage, disk_usage, cpu_usage = json_data["id"], json_data["date"], list(json_data["ram"].values()), list(json_data["disk"].values()), json_data["cpu"]["percent_used"]
    tcp_ports_info = {}
    if "tcp_ports" in json_data:
        tcp_ports_info = json_data["tcp_ports"]
        
    return check_id, check_date, ram_usage, disk_usage, cpu_usage, tcp_ports_info


def get_directory_files(directory):
    return [f for f in listdir(directory) if isfile(directory+f)]
    

def list_checks():
    check_files = get_directory_files("/var/monit/")
    if not check_files:
        print("No check file found")
        exit(0)
    check_files_output = "All check files made :\n\n"
    for file in check_files:
        check_files_output += f"  - {file} (located in /var/monit/{file})\n"
    print(check_files_output)
    exit(0)
    

def get_last_check():
    check_directory = "/var/monit/"
    check_files = get_directory_files(check_directory)
    
    if not check_files:
        print("No check file found, please make a check to get the last check values")
        exit(1)
        
    last_check_file_name = check_files[-1]
    last_check_file_path = check_directory + last_check_file_name
    last_check_file = open(last_check_file_path)
    
    check_id, check_date, ram_usage, disk_usage, cpu_usage, tcp_ports_info = read_json_file(last_check_file)
    system_check_output(check_id, check_date, ram_usage, disk_usage, cpu_usage, tcp_ports_info)
    exit(0)
    
    
def average_check_output(average_values):
    check_output = f"""
RAM: 
    Total RAM: {average_values["ram"][0]} GB
    Available RAM: {average_values["ram"][1]} GB
    Used RAM: {average_values["ram"][2]} GB
    Free RAM: {average_values["ram"][3]} GB
    Precent Used: {average_values["ram"][4]}%\n 
Disk: 
    Total Disk: {average_values["disk"][0]} GB
    Free Disk: {average_values["disk"][1]} GB
    Used Disk: {average_values["disk"][2]} GB
    Percent Used: {average_values["disk"][3]}%\n
CPU:
    Percent Used: {average_values["cpu"]}%"""
    
    
def compute_average(values):
    return float(sum(values)) / len(values)
    
    
def compute_values_average(last_hours_check_values):
    average_values = { "ram": [], "disk": [], "cpu": 0 }
    for ram_info in last_hours_check_values["ram"].values():
        average_values["ram"].append(compute_average(ram_info))
    for disk_info in last_hours_check_values["disk"].values():
        average_values["disk"].append(compute_average(disk_info))
    average_values["cpu"] = compute_average(last_hours_check_values["cpu"])
    return average_values


def get_files_values(files):
    check_values = { "ram":{"total_ram":[],"available_ram":[],"used_ram":[],"free_ram":[],"percent_used":[]},"disk":{"total_disk":[],"free_disk":[],"used_disk":[],"percent_used":[]},"cpu":[] }
    for file in files:
        json_file_values = read_json_file(open(f"/var/monit/{file}"))
        ram_usage, disk_usage, cpu_usage = json_file_values[2], json_file_values[3], json_file_values[4]
        check_values["ram"]["total_ram"].append(ram_usage[0])
        check_values["ram"]["available_ram"].append(ram_usage[1])
        check_values["ram"]["used_ram"].append(ram_usage[2])
        check_values["ram"]["free_ram"].append(ram_usage[3])
        check_values["ram"]["percent_used"].append(ram_usage[4])
        check_values["disk"]["total_disk"].append(disk_usage[0])
        check_values["disk"]["free_disk"].append(disk_usage[1])
        check_values["disk"]["used_disk"].append(disk_usage[2])
        check_values["disk"]["percent_used"].append(disk_usage[3])
        check_values["cpu"].append(cpu_usage)
    return check_values
        

def get_files_from_last_hours(hours):
    check_directory = "/var/monit/"
    check_files = get_directory_files(check_directory)
    check_files.reverse()
    
    last_datetime = datetime.now() - timedelta(hours=hours)
    last_datetime = last_datetime.strftime('%Y%m%d%H%M%S')
    
    check_files_from_last_hours = []
    
    for file_name in check_files:
        file_date = file_name[6:20]
        if int(file_date) >= int(last_datetime):
            check_files_from_last_hours.append(file_name)
    
    return check_files_from_last_hours
    

def get_average_check_values(hours):
    check_files_from_last_hours = get_files_from_last_hours(hours)
    last_hours_check_values = get_files_values(check_files_from_last_hours)
    average_check_values = compute_values_average(last_hours_check_values)
    average_check_output(average_check_values)
    exit(0)
    
    
def main():
    parser = ArgumentParser()
    args = argument_management(parser)
    
    if not file_exists('/etc/monit/monit.conf'):
        create_file("/etc/monit/", "monit.conf", { "tcp_ports": [] })
        
    if args.check is True:
        system_check()
    if args.list is True:
        list_checks()
    if args.get_last is True:
        get_last_check()
    if args.get_avg is not None:
        get_average_check_values(args.get_avg)
        
    if args.check is False and args.list is False and args.get_last is False and args.get_avg is None:
        parser.print_help()
        exit(1)

if __name__ == "__main__":
    main()