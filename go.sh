#!/usr/bin/expect

set go_name [lindex $argv 0]

set flag 0
set file [open ip.txt]
while {1} {
    set line [gets $file]
    if {[eof $file]} {
        close $file
        break
    }
    set arguments [split $line " "]
    lassign $arguments name host username password port 
    if {$name == $go_name} {
        set flag 1
        break
    }
}

if {$flag == 1} {
    # 设置超时时间  
    set timeout 10
    if {$port == 0} {
        spawn ssh $username@$host
    } else {
        spawn ssh $username@$host -p $port
    }
    # 设置超时时间  
    expect {                 
    "*yes/no" { send "yes\r"; exp_continue} 
    "*password:" { send "$password\r" }
    }
    # 交互模式,用户会停留在远程服务器上面
    interact
} else {
    puts "error: cannot find machine name $go_name"
    puts "machine    host    username    password    port   comment"
    set file [open ip.txt]
    while {1} {
        set line [gets $file]
        if {[eof $file]} {
            close $file
            break
        }
        puts $line
    }
}

