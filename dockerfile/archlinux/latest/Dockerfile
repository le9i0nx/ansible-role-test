FROM finalduty/archlinux:latest
MAINTAINER Aleksey Gavrilov <le9i0nx@gmail.com>
ENV LC_ALL C

RUN pacman -Syu systemd openssh python --noconfirm && \
    systemctl enable sshd.service

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

RUN sed -ri 's/^#PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN echo "root:000000" | chpasswd

VOLUME ["/sys/fs/cgroup"]
VOLUME ["/run"]
VOLUME ["/tmp"]
ENV container=docker
ENV init /lib/systemd/systemd
ENTRYPOINT ["/lib/systemd/systemd"]
# docker run -d --privileged -it -v /sys/fs/cgroup:/sys/fs/cgroup:ro test-archlinux-lasted

