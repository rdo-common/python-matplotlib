#! /bin/sh

version=$1

[ -z $version ] && exit 1

dir=matplotlib-${version}
file=matplotlib-${version}.tar.gz
result=matplotlib-${version}-without-extern.tar.xz

test -f $file || wget -v http://downloads.sourceforge.net/matplotlib/$file

rm -rf matplotlib-${version}
tar xzf $file

rm -vr matplotlib-${version}/extern/{agg24,CXX,qhull}
rm -vr matplotlib-${version}/lib/matplotlib/mpl-data/sample_data/lena.*

rm -f $result
tar cJf $result $dir
