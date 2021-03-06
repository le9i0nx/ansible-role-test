FROM ubuntu:14.04
MAINTAINER Aleksej Gavrilov <le9i0nx@gmail.com>
RUN echo "\n\
deb http://mirror.yandex.ru/ubuntu/ trusty main restricted universe multiverse\n \
deb http://mirror.yandex.ru/ubuntu/ trusty-updates main restricted universe multiverse\n \
deb http://mirror.yandex.ru/ubuntu/ trusty-backports main restricted universe multiverse\n \
deb-src http://mirror.yandex.ru/ubuntu/ trusty main restricted universe multiverse\n \
deb-src http://mirror.yandex.ru/ubuntu/ trusty-updates main restricted universe multiverse\n \
deb-src http://mirror.yandex.ru/ubuntu/ trusty-backports main restricted universe multiverse\n \
deb http://security.ubuntu.com/ubuntu trusty-updates main restricted universe multiverse\n \
deb-src http://security.ubuntu.com/ubuntu trusty-updates main restricted universe multiverse\n \
\n" > /etc/apt/sources.list

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update  && \
    apt-get dist-upgrade -y && \
    apt-get install -y \
        sudo openssh-server ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*  /tmp/*

RUN echo "# fake some events needed for correct startup other services\n \
description     \"In-Container Upstart Fake Events\"\n \
start on startup\n \
script\n \
	rm -rf /var/run/*.pid\n \
	rm -rf /var/run/network/*\n \
	/sbin/initctl emit stopped JOB=udevtrigger --no-wait\n \
	/sbin/initctl emit started JOB=udev --no-wait\n \
	/sbin/initctl emit runlevel RUNLEVEL=3 --no-wait\n \
end script\n" > /etc/init/fake-container-events.conf

RUN rm /usr/sbin/policy-rc.d; \
    rm /sbin/initctl; dpkg-divert --rename --remove /sbin/initctl
RUN locale-gen en_US.UTF-8 && update-locale LANG=en_US.UTF-8
RUN /usr/sbin/update-rc.d -f ondemand remove; \
    for f in \
        /etc/init/u*.conf \
        /etc/init/mounted-dev.conf \
        /etc/init/mounted-proc.conf \
        /etc/init/mounted-run.conf \
        /etc/init/mounted-tmp.conf \
        /etc/init/mounted-var.conf \
        /etc/init/hostname.conf \
        /etc/init/networking.conf \
        /etc/init/tty*.conf \
        /etc/init/plymouth*.conf \
        /etc/init/hwclock*.conf \
        /etc/init/module*.conf\
    ; do \
        dpkg-divert --local --rename --add "$f"; \
    done; \
    echo '# /lib/init/fstab: cleared out for bare-bones Docker' > /lib/init/fstab

RUN sed -ri 's/^session\s+required\s+pam_loginuid.so$/session optional pam_loginuid.so/' /etc/pam.d/sshd
RUN sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN echo "root:000000" | chpasswd

ENV container docker
CMD ["/sbin/init"]



# docker run -d -it test-ubuntu14


