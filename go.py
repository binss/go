#!/usr/bin/python
# coding=utf-8
import sys
import time
import os
import pexpect
import ConfigParser


def go():
    config = ConfigParser.ConfigParser()
    config.read("machine.conf")
    machines = config.sections()
    if len(sys.argv) != 2:
        print "GO [ERROR]: Please input the machine name!"
        print "[name]\t\t[comment]"
        for machine in machines:
            print "%s\t\t%s" % (machine, config.get(machine, "comment"))
        return

    machine = sys.argv[1]
    if machine in machines:
        host = config.get(machine, "host")
        port = config.get(machine, "port")
        user = config.get(machine, "user")
        password = config.get(machine, "password")
        dir = config.get(machine, "dir")
        comment = config.get(machine, "comment")
        
        cd_dir = ""
        dir_paths = dir.split(",\n")
        if len(dir_paths) == 1:
            cd_dir = dir_paths[0]
        else:
            while True:
                print "Please select the initial dir: "
                for i, dir_path in enumerate(dir_paths):
                    print "%i: %s" % (i + 1, dir_path)
                index = input("select: ")
                if index == 0:
                    break
                if index > 0 and index <= len(dir_paths):
                    cd_dir = dir_paths[index - 1]
                    break
                print "GO [ERROR]: Please input right index!"

        if port:
            login_command = "ssh %s@%s -p %s" % (user, host, port)
        else:
            login_command = "ssh %s@%s" % (user, host)
        server = pexpect.spawn(login_command)
        # 设置窗口大小
        rows, cols = map(int, os.popen('stty size', 'r').read().split())
        server.setwinsize(rows, cols)
        # 自动交互
        if password:
            server.expect('.*ssword:')
            server.sendline(password)
        if cd_dir:
            server.expect(['.*\#', '.*~>', '.*\$'], timeout=1800)
            server.sendline("cd %s" % cd_dir)
            print "GO [INFO]: login [%s] successfully!" % machine
        server.interact()
    else:
        print "GO [ERROR]: cannot find machine name %s!" % machine
        print "[name]\t\t[comment]"
        for machine in machines:
            print "%s\t\t%s" % (machine, config.get(machine, "comment"))

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "site-packages"))
    try:
        go()
    except Exception, e:
        print "GO [ERROR]: Exception:%s" % e
