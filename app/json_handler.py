from json import load


def read_json_file(file_path):
    """Convert json file's content to a dict and return each values.

    Args:
        file_path: the path of the file that.
    Returns:
        the average value of each RAM, disk and CPU informations.
    """
    json_data = load(file_path)
    check_id, check_date, ram_usage, disk_usage, cpu_usage = (
        json_data["id"],
        json_data["date"],
        list(json_data["ram"].values()),
        list(json_data["disk"].values()),
        json_data["cpu"]["percent_used"],
    )
    tcp_ports_info = {}
    if "tcp_ports" in json_data:
        tcp_ports_info = json_data["tcp_ports"]

    return check_id, check_date, ram_usage, disk_usage, cpu_usage, tcp_ports_info


def create_report_file_json(
    check_id, check_date, ram_usage, disk_usage, cpu_usage, tcp_ports_info
):
    total_ram, available_ram, used_ram, free_ram, percent_used_ram = ram_usage
    total_disk, free_disk, used_disk, percent_used_disk = disk_usage
    percent_used_cpu = cpu_usage
    report_json = {
        "id":check_id,
        "date":check_date,
        "ram":{
            "total_ram":total_ram,
            "available_ram":available_ram,
            "used_ram":used_ram,
            "free_ram":free_ram,
            "percent_used":percent_used_ram,},
        "disk":{
            "total_disk":total_disk,
            "free_disk":free_disk,
            "used_disk":used_disk,
            "percent_used":percent_used_disk,},
        "cpu": {"percent_used":percent_used_cpu},
    }
    if tcp_ports_info != {}:
        report_json["tcp_ports"] = tcp_ports_info

    return report_json
