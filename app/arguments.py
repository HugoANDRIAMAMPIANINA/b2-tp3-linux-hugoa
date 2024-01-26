def argument_management(parser):
    g = parser.add_mutually_exclusive_group()

    g.add_argument("-c", "--check", action="store_true", help="inspect RAM, CPU and Disk usage, check if TCP ports specified in config file (/etc/monit/monit.conf) are open and used, output the results and store these in a file located in /var/monit/")
    g.add_argument("-l", "--list", action="store_true", help="output all the check files name and path")
    g.add_argument("--get-last", action="store_true", help="output the last check file results")
    g.add_argument("--get-avg", action="store", type=int, help="output average check values since the last X hours, X is the integer value given in argument")

    return parser.parse_args()