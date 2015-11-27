#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os


# base linux server business system logs analysis class
class Analysis():
    __command = ''
    __filePath = ''
    __scan = ''

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

    def execute(self):
        try:
            popen = os.popen(self.getCommand())
            return popen.read()
        except:
            print 'Analysis execute error...'

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
