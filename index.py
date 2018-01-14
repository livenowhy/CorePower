#!/usr/bin/env python
# encoding: utf-8

import platform
from corepower import app

app.debug = True  # apache 中 main 的设置无效


def run_server():
    systype = platform.system()
    print systype
    if 'Windows' == systype:
        app.run(debug=True, threaded=True)
    elif 'Darwin' == systype:
        app.run(debug=True, port=8888, host='0.0.0.0', threaded=True)
    elif 'Linux' == systype:
        app.run(debug=True, port=8888, host='0.0.0.0', threaded=True)

if __name__ == '__main__':
    run_server()
