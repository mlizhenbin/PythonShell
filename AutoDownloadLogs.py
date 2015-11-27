#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

webCmd = 'grep \"#WebLog#\" /log/wms/wms%s.log|awk -F \" \" \'{print $8\" \"$7}\'|awk -F \"ms \" \'{print $1\" \"$2}\'|awk \'{s[$2] += $1; b[$2]++;max[$2]=max[$2]>$1?max[$2]:$1}END{ for(i in s){  print max[i], s[i]/b[i], b[i], i} }\'|awk \'%s {print $1\"ms \"int($2)\"ms \"$3\" \"$4}%s\'|sort -nr'


# base linux server business system logs analysis class
class Analysis():
    __command = ''
    __filePath = ''

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

    def execute(self):
        return ""

    def dowload(self):
        os.system("sz %s" % self.filePath)


# web request and response url profile Analysis
class WebProfileAnalysis(Analysis):
    __timeLimit = ''
    __timeLimitEnd = '}'
    __scan = ''

    def __init__(self):
        pass

    def setTimeLimit(self, timeLimit):
        self.__timeLimit = timeLimit

    def getTimeLimit(self):
        return self.__timeLimit

    def setScan(self, scan):
        self.__scan = scan

    def getScan(self):
        return self.__scan

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

    def analysis(self):
        try:
            execute = self.execute()
            print execute
            path = self.getFilePath()
            profile = open(path, "wb")
            profile.write(execute);
            profile.close()

            # call sz upload file
            os.system("sz %s" % (self.getFilePath()))
            os.system("rm -rf %s" % (self.getFilePath()))

        except IOError, e:
            print 'Analysis Web write file Error...'
            print e.args
            return None


# business log errors and exception Analysis
class ExceptionAnalysis(Analysis):
    def __init__(self):
        pass


# task job profile Analysis
class JobProfileAnalysis(Analysis):
    def __init__(self):
        pass


# open api profile Analysis
class SpiProfileAnalysis(Analysis):
    def __init__(self):
        pass


# jdbc profile Analysis
class DaoProfileAnalysis(Analysis):
    def __init__(self):
        pass


# start
if __name__ == '__main__':
    webProfile = WebProfileAnalysis()
    webProfile.setCommand(webCmd)
    webProfile.setTimeLimit("99")
    webProfile.setScan("*")
    webProfile.setFilePath("WebProfile.txt")
    webProfile.analysis()
