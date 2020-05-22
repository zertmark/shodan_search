import shodan
import os
import colorama
from colorama import *
import argparse
colorama.init()
banner="""

                  ▄▄  ▄▄▄▄▄▄▄▄                                ▄▄        ▄▄
       ██        ██   ▀▀▀▀▀███                        ██       █▄        █▄
      ██        ██        ██▀    ▄████▄    ██▄████  ███████     █▄        █▄
     ██        ██       ▄██▀    ██▄▄▄▄██   ██▀        ██         █▄        █▄
    ▄█▀       ▄█▀      ▄██      ██▀▀▀▀▀▀   ██         ██          █▄        █
   ▄█▀       ▄█▀      ███▄▄▄▄▄  ▀██▄▄▄▄█   ██         ██▄▄▄        █▄        █▄
  ▄█▀       ▄█▀       ▀▀▀▀▀▀▀▀    ▀▀▀▀▀    ▀▀          ▀▀▀▀         █▄        █▄
"""
filters="""
Please enter filter to search:
You can use/combine:
1) os:<OS_NAME>
2) port:<PORT_NUMBER>
3) country:<COUNTRY_NAME>
4) net:<IP>
5) geo: <GEO_LOCATION>
6) city:<CITY_NAME>
"""
def print_good(ip,os,port,data):
 print(Fore.GREEN+"""
\n[+] IP Adress: {}
[+] OS: {}
[+] Port: {}
[+] Data: {}
""".format(ip,os,str(port),data)+Fore.RESET) 
def print_error():
 print(Fore.RED+"[-] {}".format(text)+Fore.RESET) 
def parse_arguments():
 global port,key,file_save
 parser = argparse.ArgumentParser(description="Shodan scanner")
 parser.add_argument("--key",help="Shodan API key")
 parser.add_argument("--save",'-s',help="Save output to file")
 args = parser.parse_args()
 file_save=args.save
 key=args.key
def main():
 print(banner)
 parse_arguments()
 scan()
def scan():
 global scan
 scan=shodan.Shodan(key)
 output=""
 try:
   output=get_output(input(filters+"\nEnter filter to search:").strip())
 except Exception as error:
   print(Fore.RED+"ERROR({})".format(error)+Fore.RESET)
   exit()
 print(Fore.GREEN+"\nTotal found:{}\nPrinting output...".format(output['total'])+Fore.RESET)
 for match in output['matches']:
   print_good(match['ip_str'],match['os'],match['port'],match['data'])
 save_file(output)
def save_file(output):
 if file_save != None:
   print(Fore.GREEN+"Saving output to file {}".format(file_save)+Fore.RESET)
   with open(file_save.strip(),'a') as file:
    file.write("Total found:{}".format(output['total'])) 
    for match in output['matches']:
     file.write('\n'+str(match['ip_str'])+str(match['os'])+str(match['port'])+str(match['data']))
 exit()
def get_output(filter):
 return scan.search(filter.strip())
main()
