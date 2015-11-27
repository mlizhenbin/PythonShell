#!/usr/bin/python
# -*- coding: UTF-8 -*-
import hashlib
import os
import zlib
from ftplib import FTP
from time import strftime, localtime


# 配置
class UploadConfig():
    def __init__(self, host, userName, passWord):
        self.host = host
        self.userName = userName
        self.passWord = passWord


# ftp
class Ftp(object):
    def __init__(self, host, user, passwd, **kwargs):
        self.ftp = FTP(host=host, user=user, passwd=passwd, **kwargs)
        print(self.ftp.getwelcome())

    def download(self, path, filename, saveas=None):
        self.ftp.cwd(path)
        if not saveas:
            saveas = filename
        with open(saveas, 'wb') as localfile:
            self.ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
        print('download ' + filename)

    def upload(self, filename, path=None):
        if path:
            self.ftp.cwd(path)
        with open(filename, 'rb') as localfile:
            self.ftp.storbinary('STOR ' + filename, localfile)
        print('upload ' + filename)

    def ls(self, path):
        self.ftp.cwd(path)
        self.ftp.retrlines('LIST')

    def quit(self):
        self.ftp.quit()


# 生成临时文件
class HashWar():
    def __init__(self, filename, filesize, maxsize):
        self.filename = filename
        self.filesize = filesize
        self.maxsize = maxsize

    def hashValue(self, xhash):
        filename = self.filename
        with open(filename, 'rb') as openfile:
            while True:
                data = openfile.read(self.maxsize)
                if not data:
                    break
                xhash.update(data)
        return xhash.hexdigest()

    def crc32Value(self):
        filename = self.filename
        crc = 0
        with open(filename, 'rb') as openfile:
            while True:
                data = openfile.read(self.maxsize)
                if not data:
                    break
                crc = zlib.crc32(data, crc)
        return crc


# 本地执行命令
def getPorjectPath():
    return "/Users/a11/PycharmProjects/PythonShell/";


# 版本
def getWarVersion():
    return "V3.5.2."


# shell path
def getShell():
    return "/Users/a11/PycharmProjects/PythonShell/shell/PackageUpload.sh"


# 执行上传
def execute():
    projectPath = getPorjectPath()
    version = getWarVersion()
    os.system(getShell())
    dateStr = strftime('%Y%m%d%H%M', localtime())
    totalWarFilePath = projectPath + "wms" + version + dateStr + ".war"
    shotWarName = "wms" + version + dateStr + ".war"
    os.system("mv " + projectPath + "wms-web.war " + totalWarFilePath)

    blockSize = 1024 * 1024
    size = os.path.getsize(totalWarFilePath)
    date = strftime('%Y/%m/%d %H:%M:%S', localtime(os.path.getmtime(totalWarFilePath)))
    war = HashWar(totalWarFilePath, size, blockSize)

    # 计算 MD5 值
    md5 = war.hashValue(hashlib.md5())
    # 计算 SHA1 值
    sha1 = war.hashValue(hashlib.sha1())
    # CRC32
    crc32 = war.crc32Value()

    outs = '';
    outs += 'File path: ' + totalWarFilePath + '\n'
    outs += 'Size: ' + str(size) + ' bytes\n'
    outs += 'Date modified: ' + date + '\n'
    outs += 'MD5: ' + md5.upper() + '\n'
    outs += 'SHA1: ' + sha1.upper() + '\n'
    outs += 'CRC32: ' + str((crc32 & 0xffffffff)) + '\n\n\n'

    totalMD5FilePath = projectPath + "wms" + version + dateStr + ".MD5"
    shotMD5Name = "wms" + version + dateStr + ".MD5"
    fo = open(totalMD5FilePath, "wb")
    fo.write(outs);
    fo.close()

    os.system("chmod 777 " + totalWarFilePath)
    os.system("chmod 777 " + totalMD5FilePath)

    config = UploadConfig("172.21.106.251", "dev", "dev2014@plus")
    ftp = Ftp(config.host, config.userName, config.passWord)
    print "uploading %s..." % shotMD5Name
    ftp.upload(shotMD5Name, "/wms")
    print "uploading %s..." % shotWarName
    ftp.upload(shotWarName, "/wms")
    ftp.quit()

    os.system("rm -rf " + totalWarFilePath)
    os.system("rm -rf " + totalMD5FilePath)
    print 'ftp upload files finish.'


if __name__ == '__main__':
    execute()
