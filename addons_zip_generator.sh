#!/bin/sh

SCRIPT_PATH=`dirname $0`
cd $SCRIPT_PATH

for f in ./* ; do
  if [ -d "$f" ]; then
    version=`cat $f/addon.xml | grep "addon id" | awk '{match($0,"version=\"(.*?)\" ",a)}END{print a[1]}'`
    addon_name=`basename $f`
    echo "Plugin found: $addon_name/$addon_name-$version"
    rm -f "$addon_name/$addon_name-$version.zip"
    zip -r "$addon_name/$addon_name-$version.zip" "$addon_name" -x "*.zip"
  fi
done

python addons_xml_generator.py
