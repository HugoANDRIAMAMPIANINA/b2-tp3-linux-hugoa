#!/usr/bin/env python

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