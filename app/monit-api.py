#!/usr/bin/env python
from flask import Flask, abort, jsonify
from json import load
from file_handler import get_directory_files

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
        report_json = load(report)
        if report_json["id"] == report_id:
            return jsonify(report_json)
    abort(404)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
