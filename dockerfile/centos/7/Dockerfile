# Dockerfile for building Ansible image for CentOS 7, with as few additional software as possible.

FROM centos:centos7
ENV LC_ALL C

MAINTAINER Aleksej Gavrilov <le9i0nx@gmail.com>

RUN yum -y update && \
    yum -y install sudo openssh-server && \
    yum clean all

RUN systemctl mask \
    systemd-remount-fs.service \
    dev-hugepages.mount \
    sys-fs-fuse-connections.mount \
    systemd-logind.service \
    getty.target \
    console-getty.service \
    dev-mqueue.mount \
    sys-kernel-config.mount \
    sys-kernel-debug.mount \
    display-manager.service \
    graphical.target

RUN sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN echo "root:000000" | chpasswd

VOLUME ["/sys/fs/cgroup"]
VOLUME ["/run"]
VOLUME ["/tmp"]
ENV container=docker
#ENV init /lib/systemd/systemd
#ENTRYPOINT ["/lib/systemd/systemd"]
CMD ["/usr/sbin/init"]
#CMD  ["/usr/lib/systemd/systemd"]
# docker run -d --cap-add=SYS_ADMIN -it -v /sys/fs/cgroup:/sys/fs/cgroup:ro test-centos7

