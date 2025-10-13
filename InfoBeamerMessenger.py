import socket

class InfoBeamerMessenger:

    def __init__(self):
        self._sock = socket.create_connection(("localhost", 4444), 120)
        self._sock.setblocking(False)
        self._conn = self._sock.makefile()
        intro = self._conn.readline()

        print(intro)

        self._sock.send("Witches\n".encode())

        _next = self._conn.readline()

        print(_next)

    def getData(self):
        msg = self._conn.readline()
        return msg

    def sendWaiting(self):
        #self.sock.sendto("Witches:waiting".encode(), (self.UDP_IP, self.UDP_PORT))
        self._sock.send("waiting\n".encode())
        print("send waiting")

    def sendIntro(self):
        #self.sock.sendto("Witches:intro".encode(), (self.UDP_IP, self.UDP_PORT))
        self._sock.send("intro\n".encode())
        print("send Intro")

    def sendScare(self):
        #self.sock.sendto("Witches:scare".encode(), (self.UDP_IP, self.UDP_PORT))
        self._sock.send("scare\n".encode())
        print("send Scare")
