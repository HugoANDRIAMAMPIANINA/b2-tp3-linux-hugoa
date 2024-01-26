#!/usr/bin/env python

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
    print(check_output)