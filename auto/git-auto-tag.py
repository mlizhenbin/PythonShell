# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Zhenbin.Li'

import os
from time import strftime, localtime

# WMS版本号
TAG_VERSION = 'wmsV3.6.0.';


# 初始化git tag文件名称
def initTag():
    dateStr = strftime('%Y%m%d%H%M', localtime())
    return TAG_VERSION + dateStr;


# 执行git命令生成tag并且上传到git
def doTag():
    try:
        os.popen("git pull")
        print 'git pull finish.'

        os.popen("git push")
        print 'git pull finish.'

        branch_version = os.popen("git branch -v")
        readStr = branch_version.read()
        print readStr

        reads = readStr.split("\n")
        for read in reads:
            if "*" in read:
                print "current git branch: ", read

        tag = initTag()
        cmd = "git tag -a " + tag + " -m " + "\"" + tag + "\""
        os.system(cmd)

        os.popen("git push origin --tags")
        print 'git pull tag finish.'
        print "tag:", tag

    except:
        print 'local auto git tag error.'
        return


if __name__ == '__main__':
    print 'auto git tag start...'
    doTag()
    print 'auto git tag finish'
