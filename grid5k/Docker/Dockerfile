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
 apt-get clean && \
 rm -rf /var/lib/apt/lists/*

RUN curl https://mirrors.edge.kernel.org/pub/linux/utils/boot/syslinux/3.xx/syslinux-3.73.tar.gzls --output syslinux-3.73-pre7.tar.gz && \
tar -xvzf syslinux-3.73-pre7.tar.gz

RUN cp /usr/src/app/syslinux-3.73-pre7/com32/modules/chain.c32 /srv/tftp/chain.c32 && \
cp /usr/src/app/syslinux-3.73-pre7/com32/modules/mboot.c32 /srv/tftp/mboot.c32 && \
cp /usr/src/app/syslinux-3.73-pre7/core/pxelinux.0 /srv/tftp/pxelinux.0


COPY scripts/entrypoint.sh /usr/src/app/entrypoint.sh

RUN chmod u+x /usr/src/app/entrypoint.sh

CMD ["sleep","infinity"]

# ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
