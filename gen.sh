#!/bin/sh

V=3.212
wget https://github.com/pikvm/kvmd/archive/v${V}.tar.gz
cp v${V}.tar.gz kvmd-${V}.tar.gz

pyp2rpm kvmd-${V}.tar.gz


