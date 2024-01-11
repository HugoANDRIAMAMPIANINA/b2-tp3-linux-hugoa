from argparse import ArgumentParser
from psutil import virtual_memory, disk_usage, cpu_percent, net_connections


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

def check_tcp_ports():
    return 1111 in [i.laddr.port for i in net_connections()]
    

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
    
    check_system()

if __name__ == "__main__":
    main()