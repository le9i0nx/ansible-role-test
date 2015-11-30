#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
import subprocess
import os
import sys

def proc(cmd,time = 120,sh = True ):
    print("$".format(cmd))
    try:
        outs, errs = p.communicate(timeout=time)
    except subprocess.TimeoutExpired:
        p.kill()
        outs, errs = p.communicate()
    return outs,errs,p

ROOT_PATH=os.path.dirname(__file__)

print(proc("sudo apt-get update")[0])
print(proc("sudo apt-get install -qq sshpass")[0])
print(proc("ssh-keygen -b 2048 -t rsa -f $HOME/.ssh/id_rsa -q -N \"\"")[0])
print(proc("docker info")[0])
print(proc("docker version")[0])

with open('meta/main.yml', 'r') as f:
    doc = yaml.load(f)

for i in doc["galaxy_info"]["platforms"]:
    distrib = i["name"]
    for x in i["versions"]:
        dockerfile = "{}/../dockerfile/{}/{}/Dockerfile".format(ROOT_PATH,distrib,x)
        if os.path.exists(dockerfile):
            print(proc("docker build -f {} -t {}_{} .".format(dockerfile,distrib,x))[0])
            print(proc("docker run -d --cap-add=SYS_ADMIN -it -v /sys/fs/cgroup:/sys/fs/cgroup:ro {}_{}".format(distrib,x))[0])
        else:
            print("Critical error. Not found docker files {}".format(dockerfile))
            sys.exit(1)

proc("sleep 10")
proc("docker inspect --format '{{.Config.Image}} ansible_ssh_host={{.NetworkSettings.IPAddress}}' `docker ps -q` >> /etc/ansible/hosts")
for item in proc("docker inspect --format '{{ .NetworkSettings.IPAddress }}' \`docker ps -q\`")[0]:
    proc("ssh-keyscan -H {} >> ~/.ssh/known_hosts".format(item))
    proc("sshpass -p '000000' ssh-copy-id root@{}".format(item))

