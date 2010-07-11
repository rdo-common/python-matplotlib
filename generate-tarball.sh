#! /bin/sh

version=$1

[ -z $version ] && exit 1

dir=matplotlib-${version}
file=matplotlib-${version}.tar.gz
result=matplotlib-${version}-without-gpc.tar.gz

rm -rf matplotlib-${version}
tar xzf $file

rm matplotlib-${version}/agg24/include/agg_conv_gpc.h

rm -f $result
tar czf $result $dir
