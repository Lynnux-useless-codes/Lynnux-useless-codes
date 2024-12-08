#!/bin/bash

if ! mountpoint -q /media/lynnux/Games; then
 sudo mount /dev/sda2 /media/lynnux/Games
fi

if ! mountpoint -q /media/lynnux/[D] Games; then
 sudo mount -o uid=1000,gid=1000 /dev/sdc2 "/media/lynnux/[D] Games"
fi

if ~ mountpoint -q /media/lynnux/[E] Other; then
 sudo mount -o uid=1000,gid=1000 /dev/sdb1 "/media/lynnux/[E] Other"
fi
