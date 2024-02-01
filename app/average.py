def compute_average(values):
    """Calculate the average value from the list of values.

    Args:
        values: list of values to compute.
    Returns:
        the average value.
    """
    return float(sum(values)) / len(values)


def calcultate_averages(last_hours_check_values):
    """Calculate and add each average value in a dict and return the dict.

    Args:
        last_hours_check_values: dict with ram, disk and cpu values list to average.
    Returns:
        a dict the average value of each RAM, disk and CPU informations.
    """
    average_values = {"ram": [], "disk": [], "cpu": 0}
    for ram_info in last_hours_check_values["ram"].values():
        average_values["ram"].append(compute_average(ram_info))
    for disk_info in last_hours_check_values["disk"].values():
        average_values["disk"].append(compute_average(disk_info))
    average_values["cpu"] = compute_average(last_hours_check_values["cpu"])
    return average_values
