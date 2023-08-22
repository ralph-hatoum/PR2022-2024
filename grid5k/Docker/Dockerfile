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


COPY scripts/entrypoint.sh /usr/src/app/entrypoint.sh

RUN chmod u+x /usr/src/app/entrypoint.sh

RUN mkdir -p /run/mysqld && chown -R mysql:mysql /run/mysqld

# RUN groupadd -r mysql && useradd -r -g mysql mysql

RUN sudo service mariadb start

USER mysql


RUN mysql -h localhost -u root -p 

# TODO modify mysqlconf mainly socket path

# RUN mysql -h localhost -u root -pr00t -e "CREATE DATABASE deploy3;" && \
# mysql -h localhost -u root -p -e "GRANT select, insert, update, delete, create, drop, alter, \
# create temporary tables, lock tables ON deploy3.* \ TO 'deploy'@'kadeploy.site.grid5000.fr';"


CMD ["sleep","infinity"]

# ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
