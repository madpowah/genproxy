import socket
from threading import Thread
from cmd2 import Cmd


class bcolors:
    HEADER = '\033[95m'
    PROMPT = '\033[94m'
    TXT = '\033[93m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class myThread(Thread):
    def __init__(self, ip, port, con, target_ip, target_port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.con = con
        self.target_ip = target_ip
        self.target_port = target_port
        print("[+] New thread : " + ip + ":" + str(port))

    def run(self):
        while True:
            data = self.con.recv(2048)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.target_ip, int(self.target_port)))
            s.send(data)
            ret = s.recv(2048)
            print(ret.decode('ascii'))
            self.con.send(ret)


class Genproxy(Cmd):

    def __init__(self):
        self.target_ip = "127.0.0.1"
        self.target_port = 80

        self.local_ip = "127.0.0.1"
        self.local_port = 4242

        # On lance Cmd
        Cmd.__init__(self)
        self.last = []
        self.last.append([])
        self.prompt = bcolors.PROMPT + "GenProxy >>> " + bcolors.ENDC
        self.cmd = ""

    # Launch prompt for target informations
    def do_target_conf(self, arg, opts=None):
        self.target_ip = input("Target IP/host : ")
        self.target_port = input(" Target port : ")

    # launch prompt for local proxy information
    def do_local_conf(self, arg, opts=None):
        self.local_ip = input("IP/host to bind : ")
        self.local_port = input("Port binding : ")

    def do_start(self, arg, opts=None):
        # TCP binding
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.local_ip, int(self.local_port)))
        mythreads = []

        while True:
            s.listen(5)
            print("Server: waiting TCP connection ...")
            (con, (ip, port)) = s.accept()
            mythread = myThread(ip, port, con, self.target_ip, self.target_port)
            mythread.start()
            mythreads.append(mythread)


############# main() ###########
def main():
    shell = Genproxy()
    shell.cmdloop()


if __name__ == '__main__':
    main()
