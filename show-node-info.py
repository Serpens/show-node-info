#!/usr/bin/env python3
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from subprocess import Popen, PIPE


HTML_TEMPLATE = """<html>
<head>
<title>System info</title>
<meta http-equiv="refresh" content="5">
</head>
<body>
  <div style="width: 50%;float: left">
    <h1>top</h1>
    <pre>{0}</pre>
  </div>
  <div style="width: 50%;float: right">
    <h1>nvidia-smi</h1>
    <pre>{1}</pre>
  </div>
</body>
</html>
"""


class requestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        ps = Popen(['/usr/bin/top', '-bn1'], stdout=PIPE, stdin=PIPE,
                   stderr=PIPE, shell=False)
        top_out, top_err = ps.communicate()
        top_out = top_out.decode('utf8')

        ps = Popen(['/usr/bin/nvidia-smi'], stdout=PIPE, stdin=PIPE,
                   stderr=PIPE, shell=False)
        nvidia_out, nvidia_err = ps.communicate()
        nvidia_out = nvidia_out.decode('utf8')

        message = HTML_TEMPLATE.format(top_out, nvidia_out)
        self.wfile.write(bytes(message, 'utf8'))
        return


def run_server():
    server_address = ('0.0.0.0', 5555)
    httpd = HTTPServer(server_address, requestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
