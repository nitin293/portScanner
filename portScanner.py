import socket
import sys
import threading
import os


def banner():
    print('''
        ____            _   ____                                  
        |  _ \ ___  _ __| |_/ ___|  ___ __ _ _ __  _ __   ___ _ __ 
        | |_) / _ \| '__| __\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
        |  __/ (_) | |  | |_ ___) | (_| (_| | | | | | | |  __/ |   
        |_|   \___/|_|   \__|____/ \___\__,_|_| |_|_| |_|\___|_|   
        
                                                Author : Nitin Choudhury
        -----------------------------------------------------------------------------------
    ''')


class PortScanner:

    def __init__(self, host):
        self.host = host
        self.portList = []


    def scan(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.7)

        closed = s.connect_ex((host, port))     # if port is closed, it'll return number else return 0

        if not closed:
            self.portList.append(port)

        s.close()


    def getHost(self):
        IP = socket.gethostbyname(self.host)

        return IP


    def main(self, method):
        host = self.getHost()

        if method in ['-s', '--show']:
            print(f"[+] Starting PortScan for Host {host}\n")
            for port in range(1, 65536):
                thread = threading.Thread(target=self.scan(host, port))
                thread.start()
                thread.join()

            for openPort in self.portList:
                print(f"Open port found {openPort}")


        elif method in ['-ns', '--nmap-show']:
            print(f"[+] Starting PortScan for Host {host}\n")
            for port in range(1, 65536):
                thread = threading.Thread(target=self.scan(host, port))
                thread.start()
                thread.join()

            print(f"Open Ports : {self.portList}\n")

            portlist = ''.join(str(self.portList).split())[1:-1]
            cmd = f"nmap -sC -sV -p {portlist} {host}"
            print(f"Performing Command : {cmd}")

            os.system(cmd)


        else:
            print("[!] Invalid method !")


if __name__ == '__main__':
    try:
        hostname = sys.argv[1]
        method = sys.argv[2]
        port_scan = PortScanner(hostname)
        banner()
        port_scan.main(method)

    except IndexError:
        scriptname = sys.argv[0]
        banner()
        print(f"Usage : python3 {scriptname} [host] [method]\n\nMethods :\n\t-s\t--show\t\t\tDescription : Show result directly.\n\t-ns\t--nmap-show\t\tDescription : Use nmap for detailed enumeration of the open ports.")

    except socket.gaierror:
        print("[!] Invalid host or Check your internet connectivity.")