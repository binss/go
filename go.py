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
        print "name\t\tcomment"
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
            index = -1
            while index < 0 or index > len(dir_path):
                print "GO [ERROR]: Please input right index!"
                print "Please select the initial dir: "
                for i, dir_path in enumerate(dir_paths):
                    print "%i: %s" % (i + 1, dir_path)
                index = input("select: ")
                if index != 0:
                    cd_dir = dir_paths[index - 1]

        if port:
            login_command = "ssh %s@%s -p %s" % (user, host, port)
        else:
            login_command = "ssh %s@%s" % (user, host)
        server = pexpect.spawn(login_command)
        if password:
            server.expect('.*ssword:')
            server.sendline(password)
        if cd_dir:
            server.sendline("cd %s" % cd_dir)
        server.interact()
    else:
        print "GO [ERROR]: cannot find machine name %s!" % machine
        print "name\t\tcomment"
        for machine in machines:
            print "%s\t\t%s" % (machine, config.get(machine, "comment"))

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "site-packages"))
    go()
