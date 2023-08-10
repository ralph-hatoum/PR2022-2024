FROM ubuntu:latest

USER root

WORKDIR /usr/src/app

#Install needed libraries 
RUN apt-get update && \
apt-get -qq -y install curl && \
apt-get -qq -y install tar && \
apt-get -qq install -y python3 && \
apt-get -qq install -y python3-pip && \
apt-get -qq install -y lsof && \
apt-get -qq install -y sudo && \
apt-get -qq install -y openssh-server

## Installations relative to IPFS
    #Install IPFS binary
RUN curl https://dist.ipfs.tech/kubo/v0.22.0/kubo_v0.22.0_linux-amd64.tar.gz --output kubo_v0.22.0_linux-amd64.tar.gz && \
tar -xvzf kubo_v0.22.0_linux-amd64.tar.gz && \
kubo/install.sh && \
rm -f kubo_v0.22.0_linux-amd64.tar.gz && rm -R kubo

    #Install IPFS cluster 
RUN curl https://dist.ipfs.tech/ipfs-cluster-ctl/v1.0.6/ipfs-cluster-ctl_v1.0.6_linux-amd64.tar.gz --output ipfs-cluster-ctl_v1.0.6_linux-amd64.tar.gz && \
curl https://dist.ipfs.tech/ipfs-cluster-service/v1.0.6/ipfs-cluster-service_v1.0.6_linux-amd64.tar.gz --output ipfs-cluster-service_v1.0.6_linux-amd64.tar.gz && \
tar -xvzf ipfs-cluster-ctl_v1.0.6_linux-amd64.tar.gz && \
tar -xvzf ipfs-cluster-service_v1.0.6_linux-amd64.tar.gz && \
cp ipfs-cluster-ctl/ipfs-cluster-ctl /usr/local/bin/ipfs-cluster-ctl && \
cp ipfs-cluster-service/ipfs-cluster-service /usr/local/bin/ipfs-cluster-service && \
rm -f ipfs-cluster-ctl_v1.0.6_linux-amd64.tar.gz && rm -f ipfs-cluster-service_v1.0.6_linux-amd64.tar.gz && rm -R ipfs-cluster-service && rm -R ipfs-cluster-ctl


## Copy entrypoint + all needed scripts
RUN mkdir python_scripts
COPY scripts/entrypoint.sh /usr/src/app/entrypoint.sh
COPY scripts/requirements.txt /usr/src/app/python_scripts/requirements.txt
COPY scripts/node_exporter.py /usr/src/app/python_scripts/node_exporter.py

RUN chmod u+x /usr/src/app/entrypoint.sh 

RUN pip3 install --upgrade pip && \
pip3 install -r python_scripts/requirements.txt

EXPOSE 8080
EXPOSE 4001
EXPOSE 5001
EXPOSE 22

RUN service ssh start
RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 test 
RUN echo 'test:test' | chpasswd
CMD [ "/usr/sbin/sshd", "-D" ]

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
