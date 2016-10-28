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

def cmd_list_proc(list_proc):
    for item in list_proc:
        print("$    {}".format(item))
        out = proc(item)
        print("{}".format(out[0]))

def job(dockerf, dis , ver):
    o1_cmd = "docker run --name {0}_{1} -d --cap-add=SYS_ADMIN -it -v /sys/fs/cgroup:/sys/fs/cgroup:ro le9i0nx/ansible-role-test:{0}-{1}".format(dis,ver)
    print("$   {}".format(o1_cmd))
    o1 = proc(o1_cmd)
    print("{}".format(o1[0]))
    return

REPO = os.environ['TRAVIS_REPO_SLUG'].split('/')[1]
PWD = os.environ['PWD']

cmd_list = [
    "sudo ln -s {}/test/{} /etc/ansible".format(PWD,REPO),
    ]

cmd_list_proc(cmd_list)

with open('meta/main.yml', 'r') as f:
    doc = yaml.load(f)

ROOT_PATH=os.path.dirname(__file__)
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
    "sudo apt-get update",
    "sudo apt-get install -qq sshpass",
    "ssh-keygen -b 2048 -t rsa -f $HOME/.ssh/id_rsa -q -N \"\"",
    "sleep 10",
    "docker inspect --format '{{.Name}} ansible_host={{.NetworkSettings.IPAddress}} ansible_user=root' `docker ps -q` | sed -e 's/^.\{1\}//' >> /etc/ansible/hosts",
    "cat /etc/ansible/hosts",
    ]

cmd_list_proc(cmd_list)

for item in proc("docker inspect --format '{{ .NetworkSettings.IPAddress }}' `docker ps -q`")[0].splitlines():
    cmd_list = [
        "ssh-keyscan -H {} >> ~/.ssh/known_hosts".format(item),
        "cat ~/.ssh/known_hosts",
        "sshpass -p '000000' ssh-copy-id root@{}".format(item),
        ]
    cmd_list_proc(cmd_list)

