from flask import Flask, abort, jsonify
from json import load

from os.path import isfile, exists
from os import makedirs, listdir

app = Flask(__name__)
app.secret_key = 'my super secret key'.encode('utf8')


@app.route('/reports/<report_id>', methods=['GET'])
def get_report(report_id=None):
    check_directory = "/var/monit/"
    check_files = get_directory_files(check_directory)
    if not check_files:
        print("No check file found")
        exit(0)
    for file_name in check_files:
        report = open(check_directory+file_name)
        if report["id"] == report_id:
            return jsonify(report)
    abort(404)


def get_directory_files(directory):
    return [f for f in listdir(directory) if isfile(directory+f)]
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
