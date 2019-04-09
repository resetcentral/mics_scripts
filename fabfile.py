from fabric.api import *
from ipaddress import ip_network
import sys

env.warn_only = True

LOCAL_NET = "192.168.1.0/24"
ROOTPASS = "trojanlockdown"
PASS = "regularlockdown"
CURRENT_PASS = "Password1!"

env.user = "dsu"
env.password = CURRENT_PASS
env.sudo_password = CURRENT_PASS
env.hosts = [str(host) for host in ip_network(LOCAL_NET.decode()).hosts()]

@parallel
def linux_initial():
    put("linux-init", "linux-init")
    sudo("sh linux-init changerootpass {}".format(ROOTPASS))
    sudo("sh linux-init changepass {}".format(PASS))
    sudo("sh linux-init createuser dsu {}".format(ROOTPASS))
    sudo("sh linux-init fixsudoers root dsu {}".format(env.user))
    sudo("sh linux-init fixprofile")

    put("iptables-init", "iptables-init")
    sudo("sh iptables-init {}".format(LOCAL_NET))

    sudo("sh linux-init printpersistence > pers.txt")
    sudo("sh linux-init nophpshell")
    sudo("sh linux-init nopam")

    put("log-modtime", "log-modtime")
    put("loopit", "loopit")

    sudo("history -c")
    run("history -c")

    sudo("sh linux-init fixsshd")
    sudo("sh linux-init killconn")

@parallel
def hello():
   run("echo hello!")
