#!/usr/bin/python
# -*- coding: UTF-8 -*-

# business log errors and exception Analysis
import os

from analysis.Analysis import Analysis


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
