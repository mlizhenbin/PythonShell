#!/usr/bin/python
# -*- coding: UTF-8 -*-
import fcntl
import os
import socket
import struct


# base linux server business system logs analysis class
class Analysis():
    __command = ''
    __filePath = ''
    __scan = ''
    __outConsole = None

    def __index__(self):
        pass

    def setCommand(self, command):
        self.__command = command

    def getCommand(self):
        return self.__command

    def setFilePath(self, filePath):
        self.__filePath = filePath

    def getFilePath(self):
        return self.__filePath

    def setScan(self, scan):
        self.__scan = scan

    def getScan(self):
        return self.__scan

    def setOutConsole(self, outConsole):
        self.__outConsole = outConsole

    def getOutConsole(self):
        return self.__outConsole

    def execute(self):
        try:
            command = self.getCommand() % (self.getScan())
            print command
            popen = os.popen(command)
            return popen.read()
        except IOError, e:
            print 'Analysis execute error...'
            print e
            return None

    def analysis(self):
        try:
            execute = self.execute()
            path = self.getFilePath()
            if path == None or execute == None or execute == '':
                return

            profile = open(path, "wb")
            profile.write(execute);
            profile.close()

            # call sz upload file
            os.system("sz %s" % (self.getFilePath()))
            os.system("rm -rf %s" % (self.getFilePath()))
        except IOError, e:
            print 'Analysis Web write file Error...'
            print e
            return None


# business log errors and exception Analysis
class ErrorAnalysis(Analysis):
    __filterErrors = []
    __outConsoleColor = '--color=always'
    __outline = '10'
    __search = ''
    __suffix = ''

    def __init__(self):
        pass

    def setFilterErrors(self, filterErrors):
        self.__filterErrors = filterErrors

    def getFilterErrors(self):
        return self.__filterErrors

    def setOutline(self, outline):
        self.__outline = outline

    def getOutline(self):
        return self.__outline

    def setSearch(self, search):
        self.__search = search

    def getSearch(self):
        return self.__search

    def setSuffix(self, suffix):
        self.__suffix = suffix

    def getSuffix(self):
        return self.__suffix

    def setConsoleColor(self, consoleColor):
        self.__outConsoleColor = consoleColor

    def getConsoleColor(self):
        return self.__outConsoleColor

    def execute(self):
        try:
            errors = self.getFilterErrors()
            filterStr = ''
            if errors != None and len(errors) > 0:
                for error in errors:
                    filterStr += error
            command = self.getCommand() % (
                self.getOutline(), self.getSearch(), self.getScan(), filterStr, self.getOutline(), self.getSearch(),
                self.getConsoleColor())
            print command
            popen = os.popen(command)
            return popen.read()
        except:
            print 'Analysis Exception linux command Error...'


# web request and response url profile Analysis
class WebProfileAnalysis(Analysis):
    __timeLimit = ''
    __timeLimitEnd = '}'

    def __init__(self):
        pass

    def setTimeLimit(self, timeLimit):
        self.__timeLimit = timeLimit

    def getTimeLimit(self):
        return self.__timeLimit

    def execute(self):
        try:
            command = self.getCommand()
            limit = '{if($1>%s)' % self.getTimeLimit()
            newCmd = ''
            if self.getTimeLimit() != None:
                newCmd = command % (self.getScan(), limit, self.__timeLimitEnd)
            else:
                newCmd = command % (self.getScan(), "", "")
            print newCmd
            popen = os.popen(newCmd)
            return popen.read()
        except:
            print 'Analysis Web execute linux command Error...'
            return None


# init web
def getCommands():
    cmd = {}
    cmd[
        'webCmd'] = 'grep \"#WebLog#\" /log/wms/wms%s.log|awk -F \" \" \'{print $8\" \"$7}\'|awk -F \"ms \" \'{print $1\" \"$2}\'|awk \'{s[$2] += $1; b[$2]++;max[$2]=max[$2]>$1?max[$2]:$1}END{ for(i in s){  print max[i], s[i]/b[i], b[i], i} }\'|awk \'%s {print $1\"ms \"int($2)\"ms \"$3\" \"$4}%s\'|sort -nr'
    cmd['errorCmd'] = 'grep -%s %s /log/wms/wms%s.log%s|grep -%s %s %s'
    cmd[
        'jobCmd'] = 'grep \"success: costTime\" /log/wms/wms%s.log|awk -F \"]\" \'{print $2}\'|awk -F \".\" \'{print $11\".\"$12}\'|awk -F \" \" \'{print $3\" \"$1}\'|awk -F \"=\" \'{print $2}\'|awk -F \"ms \" \'{print $1\" \"$2}\'|awk \'{s[$2] += $1; b[$2]++;max[$2]=max[$2]>$1?max[$2]:$1}END{ for(i in s){  print max[i], s[i]/b[i], b[i], i} }\'|awk -F \" \" \'{print $1\"ms \"int($2)\"ms \"$3\" \"$4}\'|sort -nr'
    cmd[
        'spiCmd'] = 'grep \"#ConsumerLog#\" /log/wms/wms%s.log|awk -F \" \" \'{print $8\" \"$10}\'|awk -F \"ms \" \'{print $1}\'|awk -F \" \" \'{print $2\" \"$1}\'|awk \'{s[$2] += $1; b[$2]++;max[$2]=max[$2]>$1?max[$2]:$1}END{ for(i in s){  print max[i], s[i]/b[i], b[i], i} }\'|awk -F \" \" \'{print $1\" \"int($2)\"ms \"$3\" \"$4}\'|sort -nr'
    return cmd


# define execute shells
def callWebProfileAnalysis(commands, ip):
    analysis = WebProfileAnalysis()
    analysis.setCommand(commands.get("webCmd"))
    analysis.setTimeLimit("99")
    analysis.setScan("*")
    analysis.setFilePath("web_%s.txt" % (ip))
    analysis.analysis()


# init error
def callErrorAnalysis(commands, ip):
    analysis = ErrorAnalysis()
    analysis.setCommand(commands.get("errorCmd"))
    analysis.setScan("")
    analysis.setOutline("5")
    analysis.setSearch("\"Exception\"")
    filters = []
    filters.append('|grep -v \"SalesOrderDistributeException\"')
    analysis.setFilterErrors(filters)
    analysis.setFilePath("error_%s.txt" % (ip))
    analysis.analysis()


# job Analysis
def callJobAnalysis(commands, ip):
    analysis = Analysis()
    analysis.setCommand(commands.get("jobCmd"))
    analysis.setScan("*")
    analysis.setFilePath("job_%s.txt" % (ip))
    analysis.analysis()


# spi Analysis
def callSpiAnalysis(commands, ip):
    analysis = Analysis()
    analysis.setCommand(commands.get("spiCmd"))
    analysis.setScan("*")
    analysis.setFilePath("spi_%s.txt" % (ip))
    analysis.analysis()


# 计算IP地址
def handleAddress(ifName):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifName[:15])
    )[20:24])


# 获取IP地址
def getIp():
    ip = None
    try:
        ip = handleAddress("eth0")
    except:
        try:
            ip = handleAddress("em2")
        except:
            ip = socket.gethostbyname(socket.gethostname())

    if ip == None:
        ip = '127.0.0.1'
    return ip


# start
if __name__ == '__main__':
    ip = getIp()
    commands = getCommands()
    callWebProfileAnalysis(commands, ip)
    callErrorAnalysis(commands, ip)
    callJobAnalysis(commands, ip)
    callSpiAnalysis(commands, ip)
