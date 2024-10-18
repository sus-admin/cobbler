#!/bin/bash
yum -c $1/etc/yum.conf --installroot $1 update -y
yum -c $1/etc/yum.conf --installroot $1 install -y vim ipref
chroot $1 touch /root/test.txt
# # # *** OR *** # # #
# echo "touch /root/test.txt" | chroot $1 /bin/bash -s
