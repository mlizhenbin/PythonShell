#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

from analysis.Analysis import Analysis


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
