#!/usr/bin/python
# -*- coding: UTF-8 -*-
import hashlib
import os
import zlib
from ftplib import FTP
from time import strftime, localtime


class UploadConfig():
    def __init__(self, host, userName, passWord, remotePath, localPath):
        self.localPath = localPath
        self.remotePath = remotePath
        self.host = host
        self.userName = userName
        self.passWord = passWord


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


def createUploadFile():
    tempPath = "/Users/a11/PycharmProjects/PythonShell/"
    version = "V3.5.2."
    os.system("/Users/a11/PycharmProjects/PythonShell/shell/PackageUpload.sh")
    dateStr = strftime('%Y%m%d%H%M%S', localtime())
    newWarName = tempPath + "wms" + version + dateStr + ".war"
    shotWarName = "wms" + version + dateStr + ".war"
    os.system("mv " + tempPath + "wms-web.war " + newWarName)

    blockSize = 1024 * 1024
    size = os.path.getsize(newWarName)
    date = strftime('%Y/%m/%d %H:%M:%S', localtime(os.path.getmtime(newWarName)))
    war = HashWar(newWarName, size, blockSize)

    md5 = war.hashValue(hashlib.md5())  # 计算 MD5 值
    sha1 = war.hashValue(hashlib.sha1())  # 计算 SHA1 值
    crc32 = war.crc32Value()  # CRC32

    outs = '';
    outs += 'File path: ' + newWarName + '\n'
    outs += 'Size: ' + str(size) + ' bytes\n'
    outs += 'Date modified: ' + date + '\n'
    outs += 'MD5: ' + md5.upper() + '\n'
    outs += 'SHA1: ' + sha1.upper() + '\n'
    outs += 'CRC32: ' + str((crc32 & 0xffffffff)) + '\n\n\n'

    print 'File path: %s' % newWarName
    print 'Size: %s bytes' % size
    print 'Date modified: %s' % date
    # 处理结果使其中的字母大写
    print 'MD5: %s' % md5.upper()
    print 'SHA1: %s' % sha1.upper()
    print 'CRC32: %X' % (crc32 & 0xffffffff)

    newMD5Name = tempPath + "wms" + version + dateStr + ".MD5"
    shotMD5Name = "wms" + version + dateStr + ".MD5"
    fo = open(newMD5Name, "wb")
    fo.write(outs);
    fo.close()

    os.system("chmod 777 " +newWarName)
    os.system("chmod 777 " +newMD5Name)

    config = UploadConfig("172.21.106.251", "dev", "dev2014@plus", "/wmstemp", "test1112.vm")
    ftp = Ftp(config.host, config.userName, config.passWord)
    ftp.upload(shotMD5Name, "/wmstemp")
    ftp.upload(shotWarName, "/wmstemp")
    ftp.quit()


if __name__ == '__main__':
    createUploadFile()
