#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
import subprocess
import os
import sys

def proc(cmd,sh = True ):
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=sh)
    p.wait()
    outs, errs = p.communicate()
    if p.returncode:
            print(errs)
            sys.exit(1)
    return outs,errs,p

def job(dockerf, dis , ver):
    o_cmd = "docker build -f {} -t {}_{} ./zero".format(dockerf,dis,ver)
    o = proc(o_cmd)
    o1_cmd = "docker run -d --cap-add=SYS_ADMIN -it -v /sys/fs/cgroup:/sys/fs/cgroup:ro {}_{}".format(dis,ver)
    o1 = proc(o1_cmd)
    print("$    {}\n{}\n$   {}\n{}".format(o_cmd,o[0],o1_cmd,o1[0]))
    return

ROOT_PATH=os.path.dirname(__file__)

cmd_list = [
    "sudo apt-get update",
    "sudo apt-get install -qq sshpass",
    "ssh-keygen -b 2048 -t rsa -f $HOME/.ssh/id_rsa -q -N \"\"",
    "docker info",
    "docker version",
    "mkdir zero",
    ]

for item in cmd_list:
    out = proc(item)
    print("$    {}\n{}".format(item,out[0]))

with open('meta/main.yml', 'r') as f:
    doc = yaml.load(f)

for i in doc["galaxy_info"]["platforms"]:
    distrib = i["name"].lower()
    for x in i["versions"]:
        dockerfile = "{}/../dockerfile/{}/{}/Dockerfile".format(ROOT_PATH,distrib,x)
        if os.path.exists(dockerfile):
            job(dockerfile, distrib, x)
        else:
            print("Critical error. Not found docker files {}".format(dockerfile))
            sys.exit(1)

cmd_list =[
    "sleep 10",
    "docker inspect --format '{{.Config.Image}} ansible_ssh_host={{.NetworkSettings.IPAddress}}' `docker ps -q` >> /etc/ansible/hosts",
    ]
for item in cmd_list:
    out = proc(item)
    print("$ {}\n{}".format(item,out[0]))

for item in proc("docker inspect --format '{{ .NetworkSettings.IPAddress }}' `docker ps -q`")[0].splitlines():
    cmd_list = [
        "ssh-keyscan -H {} >> ~/.ssh/known_hosts".format(item),
        "sshpass -p '000000' ssh-copy-id root@{}".format(item),
        ]
    for x in cmd_list:
        out = proc(x)
        print("$ {}\n{}".format(x,out[0]))

