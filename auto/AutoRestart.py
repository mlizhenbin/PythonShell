#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

import time
import subprocess

def getPid():
    try:
        pidMessage = os.popen("ps aux|grep canvas|sort -n")
        resultStr = pidMessage.read()
        print resultStr

        split = resultStr.split("\n")
        if len(split) <= 0:
            return None

        pids = []
        for canvasPs in split:
            split_canvas = canvasPs.split(" ")
            if len(split_canvas) <= 0:
                continue

            split_bank = []
            for split_wm in split_canvas:
                if split_wm != '':
                    split_bank.append(split_wm)

            if len(split_bank) <= 0:
                continue

            pid = split_bank[1]
            print "Pid = %s" % pid
            pids.append(pid)

        if len(pids) <= 0:
            print 'Spit Pid NULL'
            return None

        print pids
        return pids
    except:
        print "Get Pid Exception!"
        return None


def stopServer(pids):
    if pids == None:
        return

    for pid in pids:
        try:
            os.system("kill -9 %s" % pid)
        except:
            print "kill pid exception"

    print "Kill all Pid finish!"


def startServer():
    subprocess.Popen("cd /opt/tomcat-canvas-8580/bin && ./startup.sh", shell=True)
    time.sleep(1)
    os.system("tail -200f /log/canvas/canvas.log")


if __name__ == '__main__':
    pids = getPid()
    stopServer(pids)
    time.sleep(1)
    startServer()
