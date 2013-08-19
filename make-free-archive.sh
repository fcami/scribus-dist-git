#! /bin/sh

if [ -z "$1" ]; then
    echo "version required"
    exit 1
fi

version=$1
nv=scribus-${version}

archive=${nv}.tar.xz
freearchive=${nv}-free.tar.xz

[ -f ${archive} ] || curl -O http://downloads.sourceforge.net/scribus/scribus-${version}.tar.xz

echo "Extracting sources ..."
rm -rf ${nv}
xzcat $archive | tar xf -

pushd ${nv}

# remove docs
rm -r scribus/doc

# remove non-free profile
rm scribus/profiles/{sRGB.icm,srgb.license}

# remove non-free content from swatches
rm resources/swatches/*.eps
rm resources/swatches/dtp-studio-free-palettes-license.rtf

rm resources/swatches/GiveLife_Color_System_*.xml
rm resources/swatches/givelife_colors_license.rtf

rm resources/swatches/Federal_Identity_Program.xml

popd

echo "Creating sources ..."
tar cf - ${nv} | xz > ${freearchive}
