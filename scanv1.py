#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Eduardo'

#
#      scanftp.py
#       
#       Copyright 2015 Eduardo Aranguiz <eduardo.aranguizolea@gmail.com>
 

import socket
import  nmap
from ftplib import FTP
import sys
import os
import errno

if "linux" in sys.platform:
  os.system("clear")
elif "win" in sys.platform:
    os.system("cls")
else:
    pass

s = socket.socket()
socket.setdefaulttimeout(2)

portList = []

class color:
    BLUE  = '\033[94m'
    GREEN = '\033[92m'
    RED   = '\033[91m'
    ENDC  = '\033[0m'

print color.BLUE +("#####################################")+color.ENDC
print color.BLUE +("#              SCAN V1.0            #")+color.ENDC
print color.BLUE +("#####################################")+color.ENDC
print

def scan(IP,PORT):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((IP,PORT))
        if PORT >= 80:
            s.send("HEAD / HTTP/1.0\r\n\r\n")
        if PORT >= 80:
            s.send('abcdefghijk\r\n')
        ans = s.recv(1024)
        return color.BLUE + ans + "[+] puerto abierto" + color.ENDC
    except socket.error as error:
        if error.errno == errno.ECONNRESET:
            return  color.BLUE + str(error) + " [+] puerto abierto" + color.ENDC
        else:
            return  color.RED +"Error tipo " + str(error) + " [-] puerto cerrado" + color.ENDC

def ftpanon(IP):
    ftp = FTP(IP)
    return ftp.login() + ftp.retrlines('LIST')
IP=raw_input("ingresa ip a consultar: ")
try:
    hostame = socket.gethostbyaddr(IP)
    print("Hostname :" + str(hostame))
except:
    pass
while True:
    PUERTO = int(raw_input("ingresa puertos, si terminaste agrega un 0: "))
    if PUERTO != 0:
        portList.append(PUERTO)
    else:
        break
FTPanon = raw_input("quieres probar acceso anonimo al servidor ftp? (si) (no) :")
FTPanon = FTPanon.lower()

for port in portList:
    nScan = nmap.PortScanner()
    resultado = scan(IP,port)
    estado = nScan.scan(IP, arguments='-n -sP -Pn -T4'+ str(port))
    estado = nScan.scan(IP, arguments='-n -sP -Pn -T4'+ str(port))
    print( "[+] revisando host "+ IP +":" + str(port)) +  "  en estado  " + estado['scan'][IP]['status']['state'] + " " + estado['nmap']['scanstats']['timestr']
    print "Banner: " + resultado
try:
    if FTPanon == "si":
        for port21 in portList:
            try:
                if port21 == 21:
                    print color.BLUE  +  ftpanon(IP)  + color.ENDC
                    print color.BLUE  +("acceso anonimo exitoso")+ color.ENDC
                else:
                    pass
            except Exception as fail:
                print("Error " + str(fail))
except:
    pass
