#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os


# base linux server business system logs analysis class
class Analysis():
    # linux shell command
    __command = ''

    # create file path
    __filePath = ''

    def __index__(self):
        pass

    def setCommand(self, command):
        self.__command = command

    def getCommand(self):
        return self.__command

    def setFilePath(self, filePath):
        self.filePath = filePath

    def getFilePath(self):
        return self.filePath

    def execute(self):
        # TODO execute linux shell
        return ""

    def dowload(self):
        os.system("sz %s" % self.filePath)


# web request and response url profile Analysis
class WebProfileAnalysis(Analysis):
    __timeLimit = ''

    def __init__(self):
        pass

    def setTimeLimit(self, timeLimit):
        self.__timeLimit = timeLimit

    def getTimeLimit(self):
        return self.__timeLimit

    def write(self, command):
        try:
            profile = open(self.filePath, "wb")
            profile.write(self.getProfileLog());
            profile.close()
        except:
            print 'Analysis Web Profile Error...'
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
    profile = WebProfileAnalysis()
    profile.setCommand("")
    profile.setFilePath("")
