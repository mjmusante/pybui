#!/usr/bin/env python3.7

from http.server import HTTPServer, BaseHTTPRequestHandler
from multiprocessing import Process, Manager
import os


from subprocess import Popen, PIPE, STDOUT
from select import poll, POLLIN

from service.serv import busywork

total = 0


class Raster(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            f"<html><body>Current total = {self.server.mydict['t']}"
            .encode('utf-8'))


def serve(d):
    server_address = ('', 8088)
    httpd = HTTPServer(server_address, Raster)
    httpd.mydict = d
    httpd.serve_forever()


def blast(pollobj, d):
    global total
    for f, e in outpoll.poll():
        if e != POLLIN:
            return False
        data = os.read(f, 256).decode(errors="replace")
        data = data.split("\n")[0]
        print(f"OUTPUT | {data} |")
        sumstr = data.split(" ")[2]
        total = sumstr.split("=")[1]
        d['t'] = total
    return True


if __name__ == "__main__":
    with Manager() as manager:
        d = manager.dict()
        s = Process(target=serve, args=(d,))
        s.start()

        p = Popen("service/serv.py", stdout=PIPE, stderr=STDOUT)
        print(f"started pid {p.pid}")
        outpoll = poll()
        outpoll.register(p.stdout.fileno(), POLLIN)
        try:
            while blast(outpoll, d):
                pass
        except KeyboardInterrupt:
            print("except")

        s.terminate()
