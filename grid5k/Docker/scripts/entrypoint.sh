#!/bin/bash

config="default-lease-time 28800; \
max-lease-time 86400; \
allow booting; \
allow bootp; \
not-authoritative; use-host-decl-names on; \
subnet 192.168.0.0 netmask 255.255.255.0 { \
option subnet-mask 255.255.255.0; \
option broadcast-address 192.168.0.255; option routers 192.168.0.254; \
option domain-name "testbed.lan"; \
filename "pxelinux.0"; \
next-server 192.168.0.1; \
host node-1.testbed.lan { \
hardware ethernet 00:09:3d:12:33:e6; \
fixed-address 192.168.0.10; \
option host-name "node-1"; \
} \
host node-2.testbed.lan { \
hardware ethernet 00:09:3d:12:33:e7; \
fixed-address 192.168.0.11; \
option host-name "node-2"; \
} }"


echo $config > /usr/local/etc/dhcpd.conf

cat /usr/local/etc/dhcpd.conf

sleep infinity