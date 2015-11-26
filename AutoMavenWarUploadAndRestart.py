#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import time
from time import strftime, localtime
import pexpect


# 格式化时间
def getDateTime():
    return strftime('%Y%m%d%H%M%S', localtime())


# SSH机器账户名称
def getIp():
    return "172.21.107.132"


# 登陆用户
def getUser():
    return "root";


# SSH PASSWORD
def getPassword():
    return "123456"


# 本地文件路径
def getFilePath():
    return "/Users/a11/Oneplus/wms/wms-web/target/wms-web.war"


# 上传目录路径
def getTargetPath():
    return "/data/www"


# 执行本地shell
def getMavenShellPath():
    return "/Users/a11/PycharmProjects/PythonShell/shell/MavenCleanAndInstall.sh"


# 上传war
def scpWar():
    print 'uploading war...'
    passwd_key = '.*assword.*'
    ip = getIp()
    user = getUser()
    filename = getFilePath()
    path = getTargetPath()
    cmdline = 'scp %s %s@%s:%s' % (filename, user, ip, path)
    try:
        child = pexpect.spawn(cmdline)
        child.expect(passwd_key)
        child.sendline(getPassword())
        child.expect(pexpect.EOF)
        print "uploading finish."
        return 0
    except:
        print "upload faild!"
        return 1


# 执行解压
def getCommands():
    commands = []
    commands.append("chmod 777 /data/www/wms-web.war")
    commands.append("rm -rf /data/www/wms*bank")
    commands.append("mv /data/www/wms /data/www/wms" + getDateTime() + "bank")
    commands.append("mkdir /data/www/wms")
    commands.append("mv /data/www/wms-web.war /data/www/wms")
    commands.append("unzip /data/www/wms/wms-web.war -d /data/www/wms")
    commands.append("rm -rf /data/www/wms/wms-web.war")
    commands.append("/opt/tomcat-wms-8580/bin/shutdown.sh")
    commands.append("/opt/tomcat-wms-8580/bin/startup.sh")
    return commands


# 远程登录虚拟机
def execute(user, ip, password, cmd):
    ssh = pexpect.spawn('ssh %s@%s "%s"' % (user, ip, cmd))
    try:
        i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=10)
        if i == 0:
            ssh.sendline(password)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            ssh.sendline(password)
        ssh.sendline(cmd)
        print ssh.read()
        return 0
    except pexpect.EOF:
        print "EOF"
        ssh.close()
        return 1
    except pexpect.TIMEOUT:
        print "TIMEOUT"
        ssh.close()
        return 1


# 执行maven 打包
def runMvn():
    try:
        os.system("chmod 777 " + getMavenShellPath())
        os.system(getMavenShellPath())
        return 0
    except Exception as e:
        print e
        return 1


# 执行脚本入口
def start():
    mvn = runMvn()
    if mvn == 1:
        return
    war = scpWar()
    if war == 1:
        return

    ip = getIp()
    password = getPassword()
    user = getUser()
    commands = getCommands()

    if execute(user, ip, password, str(commands[0])) == 1:
        return
    if execute(user, ip, password, str(commands[1])) == 1:
        return
    if execute(user, ip, password, str(commands[2])) == 1:
        return
    if execute(user, ip, password, str(commands[3])) == 1:
        return
    if execute(user, ip, password, str(commands[4])) == 1:
        return
    if execute(user, ip, password, str(commands[5])) == 1:
        return
    time.sleep(2)
    if execute(user, ip, password, str(commands[6])) == 1:
        return
    if execute(user, ip, password, str(commands[7])) == 1:
        return
        time.sleep(5)
    if execute(user, ip, password, str(commands[8])) == 1:
        return
    print "all deploy and restart wms finish!"


# 执行脚本
start()
