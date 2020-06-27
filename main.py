#!/usr/bin/env python3.7

from http.server import HTTPServer, BaseHTTPRequestHandler
from multiprocessing import Process
import os


from subprocess import Popen, PIPE, STDOUT
from select import poll, POLLIN

from service.serv import busywork

total = 0


class Raster(BaseHTTPRequestHandler):

    def do_GET(self):
        global total
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            f"<html><body>Current total = {total}".encode('utf-8'))


def serve(server_class=HTTPServer, handler_class=Raster):
    server_address = ('', 8088)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def blast(pollobj):
    global total
    for f, e in outpoll.poll():
        if e != POLLIN:
            return False
        data = os.read(f, 256).decode(errors="replace")
        data = data.split("\n")[0]
        print(f"OUTPUT | {data} |")
        sumstr = data.split(" ")[2]
        total = sumstr.split("=")[1]
    return True


if __name__ == "__main__":
    s = Process(target=serve)
    s.start()

    p = Popen("service/serv.py", stdout=PIPE, stderr=STDOUT)
    print(f"started pid {p.pid}")
    outpoll = poll()
    outpoll.register(p.stdout.fileno(), POLLIN)
    try:
        while blast(outpoll):
            pass
    except KeyboardInterrupt:
        print("except")
