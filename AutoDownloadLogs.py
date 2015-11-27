#!/usr/bin/python
# -*- coding: UTF-8 -*-

from analysis.Analysis import Analysis
from analysis.ErrorAnalysis import ErrorAnalysis
from analysis.WebProfileAnalysis import WebProfileAnalysis

webCmd = 'grep \"#WebLog#\" /log/wms/wms%s.log|awk -F \" \" \'{print $8\" \"$7}\'|awk -F \"ms \" \'{print $1\" \"$2}\'|awk \'{s[$2] += $1; b[$2]++;max[$2]=max[$2]>$1?max[$2]:$1}END{ for(i in s){  print max[i], s[i]/b[i], b[i], i} }\'|awk \'%s {print $1\"ms \"int($2)\"ms \"$3\" \"$4}%s\'|sort -nr'
errorCmd = 'grep -%s %s /log/wms/wms%s.log%s|grep -%s %s %s'


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


# init web
def callWebProfileAnalysis():
    analysis = WebProfileAnalysis()
    analysis.setCommand(webCmd)
    analysis.setTimeLimit("99")
    analysis.setScan("*")
    analysis.setFilePath("web.txt")
    analysis.analysis()


# init error
def callErrorAnalysis():
    analysis = ErrorAnalysis()
    analysis.setCommand(errorCmd)
    analysis.setScan("")
    analysis.setOutline("5")
    analysis.setSearch("\"Exception\"")
    filters = []
    filters.append('|grep -v \"SalesOrderDistributeException\"')
    analysis.setFilterErrors(filters)
    analysis.setFilePath("error.txt")
    analysis.analysis()


# start
if __name__ == '__main__':
    callWebProfileAnalysis()
    callErrorAnalysis()
