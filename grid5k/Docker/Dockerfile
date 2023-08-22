FROM debian:latest

USER root

WORKDIR /usr/src/app

RUN apt-get update && \
 apt-get install -y ruby-full && \
 apt-get install -y taktuk && \
 apt-get install -y isc-dhcp-server && \
 apt-get install -y syslinux && \
 apt-get install -y tftpd-hpa && \ 
 apt-get install -y curl && \ 
#  apt-get install -y mysql && \
 apt-get install -y catdoc && \
 apt-get install -y vim && \
 apt-get -qq -y install tar && \ 
 apt-get install -y default-mysql-server && \
 apt-get install -y default-mysql-client && \
 apt-get install -y make && \
 apt-get install -y gcc && \
 apt-get install -y sudo && \
 apt-get clean && \
 rm -rf /var/lib/apt/lists/*

RUN curl https://mirrors.edge.kernel.org/pub/linux/utils/boot/syslinux/3.xx/syslinux-3.73.tar.gz --output syslinux-3.73-pre7.tar.gz && \
tar -xvzf syslinux-3.73-pre7.tar.gz


RUN make -C /usr/src/app/syslinux-3.73 || true

RUN cp /usr/src/app/syslinux-3.73/com32/modules/chain.c32 /srv/tftp/chain.c32 && \
cp /usr/src/app/syslinux-3.73/com32/modules/mboot.c32 /srv/tftp/mboot.c32 && \
cp /usr/src/app/syslinux-3.73/core/pxelinux.0 /srv/tftp/pxelinux.0

COPY conf/dhcpd.conf /usr/local/etc/dhcpd.conf
COPY scripts/entrypoint.sh /usr/src/app/entrypoint.sh

RUN chmod u+x /usr/src/app/entrypoint.sh

RUN mkdir -p /run/mysqld && chown -R mysql:mysql /run/mysqld

#  RUN groupadd -r mysql && useradd -r -g mysql mysql

COPY conf/my.cnf /etc/mysql/my.cnf

RUN curl https://gitlab.inria.fr/grid5000/kadeploy/-/archive/v3.8.2.stable/kadeploy-v3.8.2.stable.tar.gz --output kadeploy_3.8.2.tar.gz \
&& tar -xvzf kadeploy_3.8.2.tar.gz -C kadeploy



# CMD ["sleep","infinity"]

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
