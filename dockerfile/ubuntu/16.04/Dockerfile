FROM ubuntu:16.04
MAINTAINER Aleksej Gavrilov <le9i0nx@gmail.com>
ENV LC_ALL C
ENV DEBIAN_FRONTEND noninteractive

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update  && \
    apt-get dist-upgrade -y && \
    apt-get install -y \
        sudo openssh-server locales python ca-certificates iproute2 && \
    locale-gen --purge en_US.UTF-8 && \
    echo -e 'LANG="en_US.UTF-8"\nLANGUAGE="en_US:en"\n' > /etc/default/locale && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*  /tmp/*


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
ENV init /lib/systemd/systemd
ENTRYPOINT ["/lib/systemd/systemd"]
# docker run -d --privileged -it -v /sys/fs/cgroup:/sys/fs/cgroup:ro test-ubuntu16

